from rich.console import Console
from rich.table import Table

from .scenarios import load_scenarios


def main() -> None:
    scenarios = load_scenarios()
    table = Table(title="Thermostat Eval Scenarios")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="bold")
    table.add_column("Tags", style="magenta")

    for scenario in scenarios:
        tags = ", ".join(scenario.tags) or "untagged"
        table.add_row(scenario.id, scenario.title, tags)

    Console().print(table)
