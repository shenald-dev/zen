"""Tests for zen-timer."""
from typer.testing import CliRunner
from zen.timer import app

runner = CliRunner()


def test_focus_invalid_minutes():
    """Test that focusing for less than 1 minute raises an error."""
    result = runner.invoke(app, ["0"])
    assert result.exit_code == 2
    err_msg = (
        "Invalid value for '[MINUTES]': 0 is not in the range 1<=x<=1440."
    )
    assert err_msg in result.output


def test_focus_invalid_minutes_too_high():
    """Test that focusing for more than 1440 minutes raises an error."""
    result = runner.invoke(app, ["1500"])
    assert result.exit_code == 2
    err_msg = (
        "Invalid value for '[MINUTES]': 1500 is not in the range 1<=x<=1440."
    )
    assert err_msg in result.output


def test_focus_valid_minutes(mocker):
    """Test a valid focus session."""
    # Mock time.sleep to avoid actually waiting during the test
    mocker.patch("time.sleep")

    # Mock time.monotonic to instantly advance past the duration
    # We use a generator or function so it doesn't run out of side effects
    # if rich calls it more
    def mock_monotonic():
        mock_monotonic.current += 10.0
        return mock_monotonic.current

    mock_monotonic.current = 0.0
    mocker.patch("time.monotonic", side_effect=mock_monotonic)
    result = runner.invoke(app, ["1"])
    assert result.exit_code == 0
    assert "Zen Mode Activated: 1 Minute of Deep Work" in result.output
    assert "Focus session complete" in result.output


def test_focus_valid_minutes_plural(mocker):
    """Test a valid focus session for plural minutes."""
    mocker.patch("time.sleep")

    def mock_monotonic():
        mock_monotonic.current += 10.0
        return mock_monotonic.current

    mock_monotonic.current = 0.0
    mocker.patch("time.monotonic", side_effect=mock_monotonic)
    result = runner.invoke(app, ["2"])
    assert result.exit_code == 0
    assert "Zen Mode Activated: 2 Minutes of Deep Work" in result.output
    assert "Focus session complete" in result.output


def test_focus_keyboard_interrupt(mocker):
    """Test handling of KeyboardInterrupt (Ctrl+C)."""
    # Simulate a KeyboardInterrupt on the first sleep call
    mocker.patch("time.sleep", side_effect=KeyboardInterrupt)
    mocker.patch("time.monotonic", return_value=0.0)
    result = runner.invoke(app, ["1"])
    # The application handles the interrupt gracefully, and exits with 130
    assert result.exit_code == 130
    assert "Session paused. Your focus still matters." in result.output


def test_focus_early_keyboard_interrupt(mocker):
    """Test handling of KeyboardInterrupt before rich is initialized."""
    # Simulate a KeyboardInterrupt right when Console is initialized
    mocker.patch(
        "rich.console.Console.__init__",
        side_effect=KeyboardInterrupt
    )
    result = runner.invoke(app, ["1"])
    # The application handles the interrupt gracefully and uses raw print
    assert result.exit_code == 130
    assert "Session paused. Your focus still matters." in result.output


def test_focus_double_keyboard_interrupt(mocker):
    """Test handling KeyboardInterrupt within the interrupt handler."""
    mocker.patch("time.sleep", side_effect=KeyboardInterrupt)
    mocker.patch("time.monotonic", return_value=0.0)

    def side_effect_func(*args, **kwargs):  # pylint: disable=unused-argument
        if side_effect_func.count == 2:
            raise KeyboardInterrupt
        side_effect_func.count += 1

    side_effect_func.count = 0
    mocker.patch("rich.console.Console.print", side_effect=side_effect_func)

    result = runner.invoke(app, ["1"])
    # The application gracefully handles the double interrupt and exits 130
    assert result.exit_code == 130


def test_version_flag():
    """Test that the --version flag outputs the version and exits."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "zen-timer version" in result.output


def test_version_flag_package_not_found(mocker):
    """Test that the --version flag outputs unknown if package not found."""
    import importlib.metadata  # pylint: disable=import-outside-toplevel
    mocker.patch(
        "importlib.metadata.version",
        side_effect=importlib.metadata.PackageNotFoundError
    )
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "zen-timer version unknown" in result.output


def test_focus_sleep_bounds_check(mocker):
    """Test that negative sleep intervals are bounded to 0."""
    mock_sleep = mocker.patch("time.sleep")

    original_min = min

    def mock_min(*args, **kwargs):
        # We only want to return -0.5 for timer.py calls
        # timer.py calls: min(sleep_interval, remaining)
        # sleep_interval is float, remaining is float.
        if (len(args) == 2 and isinstance(args[0], float) and
                isinstance(args[1], float)):
            # If we are in the focus loop
            if args[1] <= 60.0 and args[1] >= 0.0:
                return -0.5
        return original_min(*args, **kwargs)

    mocker.patch("builtins.min", side_effect=mock_min)

    # We need sleep to be called at least once before breaking
    def mock_monotonic():
        if mock_monotonic.call_count == 0:
            mock_monotonic.call_count += 1
            return 0.0  # Start time
        if mock_monotonic.call_count == 1:
            mock_monotonic.call_count += 1
            return 0.5  # First loop check
        if mock_monotonic.call_count == 2:
            mock_monotonic.call_count += 1
            return 0.6  # Recalculate if UI triggers, or next loop
        if mock_monotonic.call_count == 3:
            mock_monotonic.call_count += 1
            return 60.0  # Breaks loop
        mock_monotonic.call_count += 1
        return 65.0

    mock_monotonic.call_count = 0
    mocker.patch("time.monotonic", side_effect=mock_monotonic)

    result = runner.invoke(app, ["1"])

    assert result.exit_code == 0
    mock_sleep.assert_any_call(0)


def test_focus_double_keyboard_interrupt_cleanup(mocker):
    """Test handling of a double KeyboardInterrupt during cleanup."""
    mocker.patch("time.sleep", side_effect=KeyboardInterrupt)
    mocker.patch("time.monotonic", return_value=0.0)

    def mock_print(*args, **kwargs):  # pylint: disable=unused-argument
        mock_print.call_count += 1
        # Raise KeyboardInterrupt on the 3rd print call to simulate a
        # second Ctrl+C during the cleanup routine
        if mock_print.call_count == 3:
            raise KeyboardInterrupt

    mock_print.call_count = 0
    mocker.patch("rich.console.Console.print", side_effect=mock_print)

    result = runner.invoke(app, ["1"], catch_exceptions=False)
    assert result.exit_code == 130


def test_main(mocker):
    """Test that main() calls the Typer app."""
    mock_app = mocker.patch("zen.timer.app")
    # pylint: disable=import-outside-toplevel
    from zen.timer import main
    main()
    mock_app.assert_called_once()
