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
        mock_monotonic.calls += 1
        return 0.0 if mock_monotonic.calls == 1 else 60.1

    mock_monotonic.calls = 0
    mocker.patch("time.monotonic", side_effect=mock_monotonic)
    result = runner.invoke(app, ["1"])
    assert result.exit_code == 0
    assert "Zen Mode Activated" in result.output
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


def test_main(mocker):
    """Test that main() calls the Typer app."""
    mock_app = mocker.patch("zen.timer.app")
    # pylint: disable=import-outside-toplevel
    from zen.timer import main
    main()
    mock_app.assert_called_once()


def test_version_flag():
    """Test that the --version flag outputs the correct version."""
    # pylint: disable=import-outside-toplevel
    import importlib.metadata
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    try:
        version = importlib.metadata.version("zen-timer")
    except importlib.metadata.PackageNotFoundError:
        version = "unknown"
    assert f"zen-timer version {version}" in result.output
