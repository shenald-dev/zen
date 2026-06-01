"""Zen - Deep-work terminal timer."""
import time
import typer
# pylint: disable=import-outside-toplevel
# Import rich lazily inside the command for faster --help execution

app = typer.Typer(
    help="🧘 Deep-work terminal timer for focus sessions.",
    add_completion=False,
    rich_markup_mode=None,
)


def version_callback(value: bool):
    """Callback for the --version option."""
    if value:
        import importlib.metadata  # pylint: disable=import-outside-toplevel
        try:
            version = importlib.metadata.version("zen-timer")
        except importlib.metadata.PackageNotFoundError:
            version = "unknown"
        print(f"zen-timer version {version}")
        raise typer.Exit()


@app.command()
def focus(
    minutes: int = typer.Argument(
        25, min=1, max=1440, help="Minutes to focus for"
    ),
    version: bool = typer.Option(  # pylint: disable=unused-argument
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the application version and exit."
    )
):
    """Start a deep-work focus session."""
    # pylint: disable=too-many-locals
    seconds = minutes * 60
    console = None

    try:
        from rich.console import Console
        from rich.progress import (
            Progress, BarColumn, TextColumn, TimeRemainingColumn
        )
        from rich.panel import Panel

        console = Console()
        console.clear()
        minute_str = "Minute" if minutes == 1 else "Minutes"
        title = Panel.fit(
            f"[bold cyan]🧘 Zen Mode Activated: {minutes} "
            f"{minute_str} of Deep Work[/bold cyan]\n"
            "[gray]Do not disturb. No GUI, just flow.[/gray]",
            border_style="cyan",
            padding=(1, 4)
        )
        console.print(title, justify="center")
        console.print("\n")

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None, style="magenta", complete_style="cyan"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
            transient=False,
            auto_refresh=False,  # Disable background thread for performance
        ) as progress:
            task = progress.add_task("[cyan]Flow State...", total=seconds)

            start_time = time.monotonic()
            last_second = -1

            while True:
                elapsed = time.monotonic() - start_time
                remaining = seconds - elapsed

                if remaining <= 0:
                    progress.update(task, completed=seconds, refresh=True)
                    break

                # Only refresh UI when a full second has passed
                current_second = int(elapsed)
                if current_second > last_second:
                    progress.update(
                        task, completed=elapsed, refresh=True
                    )
                    last_second = current_second

                # Recalculate elapsed to natively absorb execution overhead
                elapsed = time.monotonic() - start_time
                remaining = seconds - elapsed

                # Drift-compensated sleep to maintain exact 1Hz refresh rate
                sleep_interval = 1.0 - (elapsed % 1.0)
                time.sleep(max(0, min(sleep_interval, remaining)))

        console.print("\n")
        console.bell()
        completion = Panel.fit(
            "[bold green]✨ Focus session complete. Take a break.[/bold green]",
            border_style="green"
        )
        console.print(completion, justify="center")
    except KeyboardInterrupt as exc:
        try:
            if console is not None:
                console.print("\n")
                from rich.panel import Panel
                interrupted = Panel.fit(
                    "[bold yellow]⏸️  Session paused. "
                    "Your focus still matters.[/bold yellow]",
                    border_style="yellow"
                )
                console.print(interrupted, justify="center")
            else:
                print("\n⏸️  Session paused. Your focus still matters.")
        except KeyboardInterrupt:
            pass
        raise typer.Exit(code=130) from exc


def main():
    """Main entrypoint for the CLI app."""
    app()


if __name__ == "__main__":  # pragma: no cover
    main()
