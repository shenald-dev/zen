2026-03-18 — No graceful Ctrl+C in TUI timer
   Learning: Terminal TUI apps using Rich Progress without KeyboardInterrupt handling leave the terminal in a dirty state on interrupt. This is a common gap in small CLI tools.
   Action: Always verify interrupt handling in terminal UI code. Wrap Progress/interactive blocks in try/except KeyboardInterrupt.

   #

   // ... 9579 characters truncated (middle section) ...

   y calls.
   ## 2026-05-18 — Stateful mocking for monotonic time

   Learning:
   Mocking time.monotonic() with static staggered return values (e.g., 0.0 then 60.1) is brittle when TUI libraries (like rich) make unpredictable internal timing calls. This consumes the expected values early, leaving the main loop with stale data and causing infinite test hangs.

   Action:
   Always mock monotonic time by dynamically incrementing a stateful counter on each call (e.g., mock_monotonic.current += 10.0) to guarantee time always moves forward naturally regardless of unseen internal library calls.