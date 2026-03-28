from typer.testing import CliRunner
from zen.timer import app

runner = CliRunner()

def test_focus_invalid_minutes():
    """Test that focusing for less than 1 minute raises an error."""
    result = runner.invoke(app, ["0"])
    assert result.exit_code == 2
    assert "Invalid value for '[MINUTES]': 0 is not in the range x>=1." in result.output

def test_focus_valid_minutes(mocker):
    """Test a valid focus session."""
    # Mock time.sleep to avoid actually waiting during the test
    mocker.patch("time.sleep")
    # Mock time.monotonic to instantly advance past the duration
    mocker.patch("time.monotonic", side_effect=[0.0, 60.1, 60.1])
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

def test_main(mocker):
    """Test that main() calls the Typer app."""
    mock_app = mocker.patch("zen.timer.app")
    from zen.timer import main
    main()
    mock_app.assert_called_once()
