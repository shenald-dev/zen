import pytest
from unittest.mock import patch
from typer.testing import CliRunner
from zen.timer import app

runner = CliRunner()

@patch("time.sleep")
def test_focus_command_default(mock_sleep):
    """Test the focus command with default 25 minutes."""
    result = runner.invoke(app, [])

    # Check execution success
    assert result.exit_code == 0

    # Check that time.sleep was called the expected number of times (25 * 60 = 1500)
    assert mock_sleep.call_count == 1500

    # Verify the output strings
    assert "Zen Mode Activated: 25 Minutes of Deep Work" in result.output
    assert "Focus session complete. Take a break." in result.output


@patch("time.sleep")
def test_focus_command_custom_time(mock_sleep):
    """Test the focus command with a custom number of minutes (e.g., 5)."""
    result = runner.invoke(app, ["5"])

    # Check execution success
    assert result.exit_code == 0

    # Check that time.sleep was called 5 * 60 = 300 times
    assert mock_sleep.call_count == 300

    # Verify the output strings
    assert "Zen Mode Activated: 5 Minutes of Deep Work" in result.output
    assert "Focus session complete. Take a break." in result.output


def test_focus_command_invalid_input():
    """Test the focus command with invalid input."""
    result = runner.invoke(app, ["not_a_number"])

    # Check execution failed due to invalid argument
    assert result.exit_code != 0

    assert "Invalid value for '[MINUTES]'" in result.output
