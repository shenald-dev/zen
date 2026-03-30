# Changelog

## [0.1.2] - 2026-03-30

### Changed
* **[Performance]:** Synchronized the underlying task loop's sleep duration directly with the UI refresh rate by implementing a drift-compensated sleep interval (`1.0 - (elapsed % 1.0)`). This prevents unnecessary CPU wakeups and eliminates visual timer drift during long focus sessions.

## [0.1.1] - 2026-03-27

### Changed
* **[Performance]:** Disabled the `rich` secondary background thread for rendering. Handled manual synchronous UI refreshes directly from the main process event loop. This zeroes out background context switching and thread contention.
* **[Pruned]:** Removed an unused `pytest` import from the test suite.
* **[Dependencies]:** Bumped minimum dependency baselines to `rich>=13.9.0` and `typer>=0.12.0`.
* **[Testing]:** Added missing test coverage for the root CLI app module execution path.
