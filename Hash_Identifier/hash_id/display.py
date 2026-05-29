 # rich table rendering

from rich.console import Console
from rich.table import Table
from rich import box
from rich.text import Text
import sys

console = Console()

CONF_STYLE = {
    "high":   ("bold green",  "● high  "),
    "medium": ("yellow",      "◑ medium"),
    "low":    ("dim",         "○ low   "),
}


def render(result: dict) -> int:
    """Print result to terminal. Returns exit code: 0=found, 1=non-hash, 2=unknown."""
    value = result["input"]
    truncated = value if len(value) <= 60 else value[:57] + "..."

    console.print(f"\n[bold]Input:[/bold] [dim]{truncated}[/dim]")
    console.print(f"[bold]Length:[/bold] [dim]{len(value)}[/dim]\n")

    # Non-hash path
    if result["non_hash"]:
        nh = result["non_hash"]
        console.print(f"[bold yellow]⚠ Not a hash —[/bold yellow] [yellow]{nh['name']}[/yellow]")
        console.print(f"  [dim]{nh['reason']}[/dim]\n")
        return 1

    candidates = result["candidates"]

    if not candidates:
        console.print("[bold red]✗ No matching hash format found.[/bold red]\n")
        return 2

    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold",
        padding=(0, 1),
    )
    table.add_column("Confidence", style="", width=12)
    table.add_column("Hash type",  style="bold", min_width=24)
    table.add_column("Reason",     style="dim")

    for c in candidates:
        style, label = CONF_STYLE[c["confidence"]]
        badge = Text(label, style=style)
        table.add_row(badge, c["name"], c["reason"])

    console.print(table)
    console.print()
    return 0
