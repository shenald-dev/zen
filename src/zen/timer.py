import time
import typer
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.layout import Layout
from rich.align import Align

app = typer.Typer(help="🧘 Deep-work terminal timer for focus sessions.")
console = Console()

@app.command()
def focus(minutes: int = typer.Argument(25, help="Minutes to focus for")):
    """Start a deep-work focus session."""
    seconds = minutes * 60
    
    console.clear()
    title = Panel.fit(
        f"[bold cyan]🧘 Zen Mode Activated: {minutes} Minutes of Deep Work[/bold cyan]\n[gray]Do not disturb. No GUI, just flow.[/gray]",
        border_style="cyan",
        padding=(1, 4)
    )
    console.print(Align.center(title))
    console.print("\n")

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=60, style="magenta", complete_style="cyan"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task("[cyan]Flow State...", total=seconds)
        
        while not progress.finished:
            time.sleep(1)
            progress.advance(task)
            
    console.print("\n")
    completion = Panel.fit(
        "[bold green]✨ Focus session complete. Take a break.[/bold green]",
        border_style="green"
    )
    console.print(Align.center(completion))
    
def main():
    app()

if __name__ == "__main__":
    main()
