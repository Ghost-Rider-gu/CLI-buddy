import time
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

console = Console()
cli_app = typer.Typer()

def show_splash_window(duration: float = 2.0):
    console.clear()

    splash_title = Text()
    splash_title.append("\n CLI Buddy v0.1.0", style="bold white")
    splash_title.append("\n Author <Iurii Golubnichenko aka Ghost Rider>", style="dim white")

    panel = Panel(
        splash_title,
        border_style = "bright_blue",
        padding = (1, 4),
        subtitle = "[dim]Loading ... [/dim]"
    )

    centered = Align.center(panel, vertical="middle")
    console.print(centered)
    time.sleep(duration)
    console.clear()

@cli_app.command()
def info():
    console.print("[bold] Info command [/bold]")

@cli_app.callback(invoke_without_command=True)
def main(ctx: typer.Context,
         no_splash: bool = typer.Option(False, "--no-splash", help="Skip splash screen")
         ):
    if ctx.invoked_subcommand is None or not no_splash:
        show_splash_window()

if __name__ == "__main__":
    cli_app()
