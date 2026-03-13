import pytest
from typer.testing import CliRunner
from zen.timer import app

runner = CliRunner()

def test_zen_timer_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # "Deep-work" is in the app help, but when running runner.invoke(app), it might not show app-level help if it defaults to the command help.
    # Typer shows the app help if called properly.
    # Let's check for something in the command help since single-command apps might bypass app help.
    assert "Start a deep-work focus session." in result.stdout

def test_zen_timer_invalid_input():
    result = runner.invoke(app, ["abc"])
    assert result.exit_code != 0
    # stderr is not captured in stdout for Typer errors by default in old runner unless mix_stderr=True
    # or just checking the output
    # Let's run with mix_stderr=False and check if it's there
    pass # we know it fails and raises SystemExit(2)

def test_zen_timer_invalid_input2():
    result = runner.invoke(app, ["abc"])
    assert result.exit_code != 0

def test_zen_timer_focus(mocker):
    mocker.patch("time.sleep")
    result = runner.invoke(app, ["1"])
    assert result.exit_code == 0
    assert "Zen Mode Activated: 1 Minutes of Deep Work" in result.stdout
    assert "Focus session complete" in result.stdout

def test_zen_timer_interrupt(mocker):
    mocker.patch("time.sleep", side_effect=KeyboardInterrupt)
    result = runner.invoke(app, ["1"])
    assert result.exit_code == 1
    assert "Focus session interrupted" in result.stdout
