## 2024-05-24 - Graceful Terminal Exits
**Learning:** Terminal applications often overlook the user experience of abrupt exits (like `Ctrl+C`). A raw `KeyboardInterrupt` traceback is jarring.
**Action:** Always wrap long-running foreground tasks in a `try...except KeyboardInterrupt` block and provide a gentle, formatted exit message to acknowledge the user's action.
