2026-03-18 — No graceful Ctrl+C in TUI timer
Learning: Terminal TUI apps using Rich Progress without KeyboardInterrupt handling leave the terminal in a dirty state on interrupt. This is a common gap in small CLI tools.
Action: Always verify interrupt handling in terminal UI code. Wrap Progress/interactive blocks in try/except KeyboardInterrupt.
