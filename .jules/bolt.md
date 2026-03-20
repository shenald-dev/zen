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

## 2024-05-25 — Synchronize Loop Wakeups with Progress Refresh Rate

Learning:
Even if a `Progress` bar is configured with `refresh_per_second=1`, the underlying task loop may still be running frequently (e.g., `time.sleep(0.1)` to poll 10 times a second). This burns unnecessary CPU cycles on wakeups that don't trigger a visual update.

Action:
Synchronize the loop's sleep duration dynamically with the remaining time, up to a maximum of `1.0 / refresh_per_second`. For a 1Hz UI, sleeping `min(1.0, remaining)` reduces loop evaluations by 10x without sacrificing timer responsiveness or accuracy.
