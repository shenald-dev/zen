import pytest
from typer.testing import CliRunner
from zen.timer import app, main

runner = CliRunner()

def test_focus_default_minutes(mocker):
    # Mock time.sleep to avoid actually waiting during tests
    mock_sleep = mocker.patch("time.sleep")

    # Run the default focus command
    result = runner.invoke(app, []) # default is 25 minutes

    assert result.exit_code == 0
    assert "Zen Mode Activated" in result.stdout
    assert "25 Minutes of Deep Work" in result.stdout
    assert "Focus session complete" in result.stdout

def test_focus_custom_minutes(mocker):
    # Mock time.sleep to avoid actually waiting
    mock_sleep = mocker.patch("time.sleep")

    # Run the focus command with a specific number of minutes
    result = runner.invoke(app, ["5"])

    assert result.exit_code == 0
    assert "Zen Mode Activated" in result.stdout
    assert "5 Minutes of Deep Work" in result.stdout
    assert "Focus session complete" in result.stdout

def test_focus_help():
    # Run the focus command with --help
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Start a deep-work focus session." in result.stdout
    assert "Minutes to focus for" in result.stdout

def test_main_runs(mocker):
    # Mock the typer app invocation inside main
    mock_app = mocker.patch("zen.timer.app")
    main()
    mock_app.assert_called_once()
