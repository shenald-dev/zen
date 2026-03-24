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
