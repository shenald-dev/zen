2026-03-18 — No graceful Ctrl+C in TUI timer
Learning: Terminal TUI apps using Rich Progress without KeyboardInterrupt handling leave the terminal in a dirty state on interrupt. This is a common gap in small CLI tools.
Action: Always verify interrupt handling in terminal UI code. Wrap Progress/interactive blocks in try/except KeyboardInterrupt.

## 2024-05-24 — Progress Bar Render Bottleneck

Learning:
Rich's `Progress` bar defaults to 10Hz rendering which incurs unnecessary CPU overhead and function calls when the underlying task only updates once per second (as is the case in our timer).

Action:
Explicitly set `refresh_per_second=1` in `Progress` instantiations whenever the task granularity is low to save CPU cycles without visibly impacting UX.

## 2024-03-19 — Replace time.sleep() with time.monotonic() for timer accuracy

Learning:
Relying on cumulative `time.sleep(1)` loops in Python is inherently inaccurate due to the time overhead of rendering/execution and system scheduling. Over a 25+ minute focus session, the timer can drift significantly, meaning it ends later than exactly 25 real-world minutes.

Action:
Always use `time.monotonic()` (or `time.time()`) to calculate total elapsed time when building accurate timers or measurement tools, updating the progress based on `elapsed_time = current_time - start_time`, rather than summing sleep intervals.

## 2025-02-23 — Reduced CPU Wakeups in Timer Loop

Learning:
The `rich.progress.Progress` instance was configured for a 1Hz refresh rate (`refresh_per_second=1`), but the main focus loop was hardcoded to sleep for 0.1 seconds per iteration (`time.sleep(0.1)`). This meant the CPU woke up 10 times per second for no functional benefit, a common inefficiency in CLI/TUI apps.

Action:
Future timer or polling loops should calculate remaining time (`remaining = total - elapsed`) and sleep dynamically based on the UI refresh rate (e.g., `time.sleep(min(1.0, remaining))`), rather than busy-waiting with small static sleep intervals. This reduces battery drain and CPU usage while maintaining accuracy.

## 2026-03-20 — Lazy Loading Heavy Imports for CLI Startup Performance

Learning:
Importing heavy UI libraries like `rich` at the module level in Typer/CLI applications causes noticeable startup delay (~300-500ms) for fast commands like `--help`.

Action:
Move heavy, non-essential imports (e.g., `rich` components and instantiations) inside the actual command handler functions to lazy-load them only when the command is run.

## 2026-03-20 — Standardized POSIX Exit Code for KeyboardInterrupt

Learning:
Catching a `KeyboardInterrupt` (Ctrl+C) and exiting normally (code 0) breaks standard POSIX expectations, making calling scripts think the command succeeded.

Action:
When catching a `KeyboardInterrupt` to cleanly handle terminal interruptions without tracebacks, always explicitly raise `typer.Exit(code=130)` (or `sys.exit(130)`) to correctly signal a SIGINT termination.

## 2024-03-24 — Typer Validation and Loop Redundancies

Learning:
Manually validating CLI arguments inside the command function bypasses the robust, built-in validation of Typer/Click, leading to inconsistent error exit codes (1 instead of 2) and custom boilerplate code. Additionally, `rich.progress` handles background thread rendering, meaning duplicate state calculations (`time.monotonic()`) inside the hot loop to try and keep the progress bar updated instantly are redundant and waste CPU cycles.

Action:
Always use `typer.Argument` constraints (like `min=1`) to handle input validation automatically and keep the logic focused on domain logic. When writing loops with sleep and external renderers, calculate elapsed time once per iteration to avoid unnecessary syscalls.

## 2026-03-26 — Prevent Background Threads in Rich CLI Wait Loops

Learning:
Rich's `Progress` component defaults to `auto_refresh=True`, which spawns a secondary background thread to handle terminal rendering. In simple blocking loops (like timers or sleep waiters), this introduces unnecessary thread contention, syscalls, and context switching overhead.

Action:
When the main thread is already responsible for updating state in a loop and sleeping, instantiate `Progress(auto_refresh=False)` to prevent the secondary thread from spawning. Explicitly trigger `progress.update(..., refresh=True)` within the main loop to handle rendering synchronously.

## 2026-03-29 — Optimize rich.progress rendering
Learning:
When using `rich.progress.Progress` for slow-updating CLI apps (like a 1-second timer loop), leaving `auto_refresh=True` enabled causes the background thread to run continuously, wasting CPU cycles and sometimes causing testing artifacts where mocks need to account for unpredictable background thread calls.

Action:
Disable the background thread by setting `auto_refresh=False` and manually call `progress.refresh()` inside the synchronous hot loop after `progress.update()`. This aligns UI refreshes exactly with state updates, improving performance and making test behavior more deterministic.

## 2026-03-30 — Synchronous Progress Render Drift and `refresh=True`
Learning:
When rendering `rich` progress bars synchronously via `progress.update(...)` inside a loop, calling `progress.refresh()` separately is less efficient than passing `refresh=True` directly to `update()`. Furthermore, simply doing `time.sleep(1.0)` inside the loop causes visual drift, as the time taken to render pushes the start of the next sleep interval further away from the exact whole second.
Action:
Always use `progress.update(..., refresh=True)` to combine update and render in a single operation when `auto_refresh=False`. To fix visual drift in manual sleep loops, compensate for execution overhead with `sleep_interval = 1.0 - (elapsed % 1.0)`.

## 2025-04-02 — Input Validation for Unbounded Loops

Learning:
When accepting numeric arguments that directly dictate loop durations or allocations (like `minutes` to focus for), omitting an upper bound (`max=1440`) allows extreme values. Even if integer overflow is not a concern in Python, extreme durations can cause floating-point drift or represent an obvious user typo that the application should handle gracefully instead of running blindly.

Action:
Always enforce reasonable, domain-specific upper bounds (`max=...`) on numeric arguments, even if the lower bound (`min=...`) is already checked.

2024-04-02 — Drift-compensated tight loop throttling
Learning: Disabling `rich.progress` auto-refresh and manually calling `refresh=True` inside a drift-compensated sleep loop is not enough to prevent high CPU utilization. If the sleep undershoots slightly, the `while True:` loop spins rapidly without sleeping meaningfully, resulting in hundreds of redundant terminal renders and pegging the CPU.
Action: Always couple drift-compensated sleep with an explicit state check (e.g., `current_second > last_second`) to throttle expensive manual operations (like terminal I/O) within the loop, guaranteeing they only fire at the intended boundary regardless of sleep inaccuracies.

## 2026-04-04 — Drift-compensated Sleep Rendering Overhead
Learning:
When manually syncing terminal UI updates (e.g., `progress.update(..., refresh=True)`) before a drift-compensated `time.sleep()`, the execution time of the rendering block acts as an uncounted overhead if the sleep interval is calculated *before* rendering. This causes the loop to consistently oversleep by the exact duration of the render step.

Action:
Always recalculate elapsed time (`time.monotonic()`) immediately *after* the synchronous UI render and right *before* calculating and invoking the sleep interval to natively absorb execution overhead.

## 2026-04-06 — Typer Shell Completion Overhead

Learning:
By default, `typer.Typer()` initializes shell completion logic (`click.shell_completion`, `shellingham`, etc.) which introduces a minor but measurable overhead (~40-50ms) to CLI startup and pollutes the `--help` menu with `--install-completion` and `--show-completion` flags.

Action:
For simple, single-command utilities where shell completion is unlikely to be used or needed, instantiate the app with `typer.Typer(add_completion=False)` to squeeze out extra startup performance and simplify the help menu.

## 2026-04-12 — Handling temporary agent files
Learning:
When testing code during a run, creating temporary root-level files (e.g. `version_test.py`) litters the repository and fails pre-commit code review checks, as they appear as unnecessary edits that degrade codebase cleanliness.
Action:
Do not leave temporary agent artifacts or scratchpad scripts in the repository. Ensure they are explicitly deleted (e.g., `rm test.py`) before requesting a code review or finalizing commits.

## 2026-04-20 — Typer Rich Markup Import Overhead

Learning:
By default, Typer attempts to import the `rich` library at module load time if it is available, in order to render help text with rich markup. This eager import blocks startup and can add up to ~100-200ms overhead, which is particularly noticeable for fast commands like `--help` or `--version`.

Action:
For simple CLI tools where rich help text formatting is not strictly required, pass `rich_markup_mode=None` to the `typer.Typer()` initialization to prevent Typer from eagerly loading `rich` on startup, yielding a measurable performance boost.

## 2026-05-18 — Stateful mocking for monotonic time
Learning: Mocking time.monotonic() with static staggered return values (e.g., 0.0 then 60.1) is brittle when TUI libraries (like rich) make unpredictable internal timing calls. This consumes the expected values early, leaving the main loop with stale data and causing infinite test hangs.
Action: Always mock monotonic time by dynamically incrementing a stateful counter on each call (e.g., mock_monotonic.current += 10.0) to guarantee time always moves forward naturally regardless of unseen internal library calls.
## 2026-05-27 — Progress Bar UX Fix

Learning:
In time-based loops using `rich.progress.Progress`, if the loop breaks as soon as elapsed time exceeds the target, the progress bar may not visually reach 100% before terminating.

Action:
Explicitly update the progress bar to 100% immediately before the `break` statement in time-based loops.
