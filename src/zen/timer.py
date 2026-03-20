import time
import typer
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.align import Align

app = typer.Typer(help="🧘 Deep-work terminal timer for focus sessions.")
console = Console()

@app.command()
def focus(minutes: int = typer.Argument(25, help="Minutes to focus for")):
    """Start a deep-work focus session."""
    if minutes < 1:
        console.print("[bold red]Error:[/bold red] Focus duration must be at least 1 minute.")
        raise typer.Exit(code=1)

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
            while not progress.finished:
                elapsed = time.monotonic() - start_time
                remaining = seconds - elapsed

                if remaining <= 0:
                    progress.update(task, completed=seconds)
                    break

                # Align sleep duration with 1Hz refresh rate to reduce CPU wakeups by 10x
                time.sleep(min(1.0, remaining))

                elapsed = time.monotonic() - start_time
                progress.update(task, completed=min(elapsed, seconds))

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
    
def main():
    app()

if __name__ == "__main__":
    main()
