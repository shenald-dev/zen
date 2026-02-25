"""
Zen: Find your flow.
"""
import time
import sys
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn

console = Console()

def focus_timer(minutes):
    seconds = minutes * 60
    console.print(f"[bold green]🧘 Zen Mode Activated.[/bold green] Focus for {minutes} minutes.")
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        refresh_per_second=1
    ) as progress:
        task = progress.add_task("[cyan]Flowing...", total=seconds)
        
        while not progress.finished:
            time.sleep(1)
            progress.update(task, advance=1)
            
    console.print("\n[bold gold1]🚀 Flow complete.[/bold gold1] Take a breath.")

if __name__ == "__main__":
    try:
        mins = int(sys.argv[1]) if len(sys.argv) > 1 else 25
        focus_timer(mins)
    except ValueError:
        console.print("[bold red]Error:[/bold red] Please provide a valid number of minutes.")
    except KeyboardInterrupt:
        console.print("\n[bold red]Zen interrupted.[/bold red] Returning to the noise.")
