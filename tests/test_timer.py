import pytest
from typer.testing import CliRunner
from zen.timer import app

runner = CliRunner()

def test_focus_success(mocker):
    # Mock time.sleep to run instantly
    mocker.patch('time.sleep', return_value=None)
    result = runner.invoke(app, ["1"])
    assert result.exit_code == 0
    assert "Zen Mode Activated: 1 Minutes of Deep Work" in result.stdout
    assert "Focus session complete. Take a break." in result.stdout

def test_focus_invalid_minutes():
    result = runner.invoke(app, ["--", "-1"])
    # Typer should reject < 1
    assert result.exit_code != 0

def test_focus_keyboard_interrupt(mocker):
    # Mock time.sleep to raise KeyboardInterrupt
    mocker.patch('time.sleep', side_effect=KeyboardInterrupt)
    result = runner.invoke(app, ["1"])
    assert result.exit_code == 0
    assert "Focus session interrupted" in result.stdout
