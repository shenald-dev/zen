# Changelog

## [0.1.9] - 2026-04-14

### Changed
* **[Assurance]:** Validated repository stability and identified structural QA improvements.
* **[Maintainability]:** Added explicit `.coveragerc` rules to exclude CLI entrypoint modules from test coverage reports, improving output clarity.
* **[Maintainability]:** Added missing `.pytest_cache/` entry to `.gitignore` to prevent test artifacts from polluting source control.
* **[Release]:** Cut release v0.1.9 to conclude the lifecycle assessment.

## [0.1.7] - 2026-04-05

### Changed
* **[Assurance]:** Validated stability of the timer loop optimization that removed redundant time recalculations. No functional regressions were detected.
* **[Release]:** Cut release v0.1.7 to formalize the lifecycle assessment and finalize codebase stabilization.

## [0.1.6] - 2026-04-03

### Changed
* **[Assurance]:** Validated stability of the recent drift-compensated sleep loop and manual UI refresh optimization. No functional regressions were detected.
* **[Pruned]:** Removed `test_cpu.py`, a development scratchpad file left over from the performance optimization run.
* **[Release]:** Cut release v0.1.6 to conclude lifecycle pruning and stabilize the build.

## [0.1.5] - 2026-04-02

### Changed
* **[Assurance]:** Validated codebase structural integrity, ran adversarial QA, and ensured testing and static analysis fully pass. No regressions or dead code found after previous optimization agent's run.
* **[Release]:** Cut release v0.1.5 to formalize the lifecycle assessment and finalize codebase stabilization.

## [0.1.4] - 2026-03-31

### Changed
* **[Bugfix]:** Addressed an edge case where an extremely early `KeyboardInterrupt` during `rich.console` initialization would raise `UnboundLocalError` by pre-defining `console` and implementing a raw print fallback.
* **[Pruned]:** Removed empty, unused `__init__.py` module from the root project directory.

## [0.1.3] - 2026-03-31

### Changed
* **[Bugfix]:** Expanded `try...except KeyboardInterrupt` block to encapsulate all terminal interactions, preventing unhandled exceptions and dirty terminal state if the user triggers an interrupt immediately upon startup.
* **[Performance]:** Improved progress bar synchronous rendering by using `refresh=True` natively within `progress.update(...)`, saving redundant rendering cycles.

## [0.1.2] - 2026-03-30

### Changed
* **[Performance]:** Synchronized the underlying task loop's sleep duration directly with the UI refresh rate by implementing a drift-compensated sleep interval (`1.0 - (elapsed % 1.0)`). This prevents unnecessary CPU wakeups and eliminates visual timer drift during long focus sessions.

## [0.1.1] - 2026-03-27

### Changed
* **[Performance]:** Disabled the `rich` secondary background thread for rendering. Handled manual synchronous UI refreshes directly from the main process event loop. This zeroes out background context switching and thread contention.
* **[Pruned]:** Removed an unused `pytest` import from the test suite.
* **[Dependencies]:** Bumped minimum dependency baselines to `rich>=13.9.0` and `typer>=0.12.0`.
* **[Testing]:** Added missing test coverage for the root CLI app module execution path.

## [0.1.8] - 2026-04-11

### Changed
* **[Assurance]:** Validated stability of the recent changes.
* **[UI]:** Allow the progress bar to dynamically resize by setting `bar_width=None`. Add a visual/audible terminal bell via `console.bell()` upon session completion.
* **[Release]:** Cut release v0.1.8.
