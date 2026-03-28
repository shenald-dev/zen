import time
import typer

app = typer.Typer(help="🧘 Deep-work terminal timer for focus sessions.")

@app.command()
def focus(minutes: int = typer.Argument(25, min=1, help="Minutes to focus for")):
    """Start a deep-work focus session."""
    from rich.console import Console
    from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
    from rich.panel import Panel
    from rich.align import Align

    console = Console()

    seconds = minutes * 60

    console.clear()
    title = Panel.fit(
        f"[bold cyan]🧘 Zen Mode Activated: {minutes} Minutes of Deep Work[/bold cyan]\n[gray]Do not disturb. No GUI, just flow.[/gray]",
        border_style="cyan",
        padding=(1, 4)
    )
    console.print(Align.center(title))
    console.print("\n")

    try:
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=60, style="magenta", complete_style="cyan"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
            transient=False,
            refresh_per_second=1,  # Optimize rendering for 1-second updates
        ) as progress:
            task = progress.add_task("[cyan]Flow State...", total=seconds)

            start_time = time.monotonic()
            while True:
                current_time = time.monotonic()
                elapsed = current_time - start_time
                remaining = seconds - elapsed

                progress.update(task, completed=min(elapsed, seconds))

                if remaining <= 0:
                    break

                time.sleep(min(1.0, remaining))

        console.print("\n")
        completion = Panel.fit(
            "[bold green]✨ Focus session complete. Take a break.[/bold green]",
            border_style="green"
        )
        console.print(Align.center(completion))
    except KeyboardInterrupt:
        console.print("\n")
        interrupted = Panel.fit(
            "[bold yellow]⏸️  Session paused. Your focus still matters.[/bold yellow]",
            border_style="yellow"
        )
        console.print(Align.center(interrupted))
        raise typer.Exit(code=130)
    
def main():
    app()

if __name__ == "__main__":
    main()
