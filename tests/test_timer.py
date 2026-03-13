import pytest
from typer.testing import CliRunner
from zen.timer import app

runner = CliRunner()

def test_focus_zero_minutes():
    """Test that zero minutes is rejected."""
    result = runner.invoke(app, ["focus", "0"])
    assert result.exit_code != 0
    assert "1" in result.stdout
    assert "min" in result.stdout.lower()

def test_focus_negative_minutes():
    """Test that negative minutes are rejected."""
    result = runner.invoke(app, ["focus", "-1"])
    assert result.exit_code != 0
    assert "1" in result.stdout
    assert "min" in result.stdout.lower()

def test_focus_valid_minutes():
    """Test that valid minutes work (we'll mock time.sleep to make it fast)."""
    import unittest.mock as mock
    with mock.patch("time.sleep", return_value=None):
        # Use a very small number if possible, or just mock the whole progress loop if needed
        # Since we just want to see it starts and finishes
        # But focus(1) will take 60 iterations.
        # Let's just check it starts correctly.
        result = runner.invoke(app, ["focus", "1"])
        assert result.exit_code == 0
        assert "Zen Mode Activated: 1 Minutes" in result.stdout
        assert "Focus session complete" in result.stdout
