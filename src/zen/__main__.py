# src/zen/__main__.py
"""Main entry point for executing zen as a module.

This module serves as the command-line interface (CLI) entry point.
It delegates execution to `zen.timer.main`, which is responsible for
parsing the new CLI flags and executing the updated timer behavior.
"""
from zen.timer import main  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    # Invoke the main function to process CLI flags and execute the updated behavior
    main()
