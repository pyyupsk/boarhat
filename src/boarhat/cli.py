"""CLI tool for running scrapers."""

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from boarhat.scrapers import CharacterScraper

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Boarhat - Duet Night Abyss Data Scraper."""
    pass


@cli.command()
@click.option(
    "--source",
    "-s",
    default="https://boarhat.gg/games/duet-night-abyss/character/",
    help="URL or file path to scrape",
)
@click.option(
    "--output",
    "-o",
    "output_dir",
    type=click.Path(path_type=Path),
    default=Path("data/processed"),
    help="Output directory",
)
@click.option(
    "--no-cache",
    is_flag=True,
    help="Force fetch from URL (ignore cache)",
)
def characters(source: str, output_dir: Path, no_cache: bool):
    """Scrape character data from boarhat.gg."""
    cache_dir = Path("data/raw")

    # Clear cache if requested
    if no_cache and isinstance(source, str) and source.startswith("http"):
        cache_file = cache_dir / "characters.html"
        if cache_file.exists():
            cache_file.unlink()
            console.print(f"[yellow]Cleared cache: {cache_file}[/yellow]")

    scraper = CharacterScraper(source, output_dir, cache_dir)
    data, output_path = scraper.run()

    # Display summary
    table = Table(title="Character Summary")
    table.add_column("Attribute", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Characters", str(len(data)))

    # Count by element
    from collections import Counter

    elements = Counter(c.element for c in data)
    table.add_row("Elements", ", ".join(f"{k}: {v}" for k, v in elements.most_common()))

    # Count by role
    roles = Counter(c.role for c in data)
    table.add_row("Roles", ", ".join(f"{k}: {v}" for k, v in roles.most_common()))

    # Count by rarity
    rarities = Counter(c.rarity for c in data)
    table.add_row("Rarities", ", ".join(f"{k}: {v}" for k, v in rarities.most_common()))

    console.print(table)
    console.print(f"\n✓ Data saved to: [bold green]{output_path}[/bold green]")


@cli.command()
def list_scrapers():
    """List available scrapers."""
    table = Table(title="Available Scrapers")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Status", style="yellow")

    table.add_row("characters", "Scrape character data", "✓ Available")
    table.add_row("weapons", "Scrape weapon data", "⚠ Not implemented")
    table.add_row("geniemon", "Scrape geniemon data", "⚠ Not implemented")
    table.add_row("demon-wedge", "Scrape demon wedge data", "⚠ Not implemented")

    console.print(table)


@cli.command()
@click.option(
    "--output",
    "-o",
    "output_dir",
    type=click.Path(path_type=Path),
    default=Path("data/processed"),
    help="Output directory",
)
@click.option(
    "--no-cache",
    is_flag=True,
    help="Force fetch from URLs (ignore cache)",
)
def all(output_dir: Path, no_cache: bool):
    """Run all available scrapers."""
    console.print("[bold yellow]Running all scrapers...[/bold yellow]\n")

    cache_dir = Path("data/raw")

    # Characters
    try:
        if no_cache:
            cache_file = cache_dir / "characters.html"
            if cache_file.exists():
                cache_file.unlink()

        source = "https://boarhat.gg/games/duet-night-abyss/character/"
        scraper = CharacterScraper(source, output_dir, cache_dir)
        scraper.run()
    except Exception as e:
        console.print(f"[red]✗ Error scraping characters: {e}[/red]")

    console.print("\n[bold green]✓ All scrapers completed![/bold green]")


if __name__ == "__main__":
    cli()
