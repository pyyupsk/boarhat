"""CLI tool for running scrapers."""

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from boarhat.scrapers import CharacterScraper, GeniemonScraper, WeaponScraper
from boarhat.scrapers.character_detail import CharacterDetailScraper

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Boarhat - Duet Night Abyss Data Scraper."""
    pass


@cli.group()
def character():
    """Character data commands."""
    pass


@character.command("list")
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
def character_list(source: str, output_dir: Path, no_cache: bool):
    """Scrape character list from boarhat.gg."""
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


@character.command("all")
@click.option(
    "--output",
    "-o",
    "output_dir",
    type=click.Path(path_type=Path),
    default=Path("data/processed/characters"),
    help="Output directory",
)
@click.option(
    "--no-cache",
    is_flag=True,
    help="Force fetch from URLs (ignore cache)",
)
def character_all(output_dir: Path, no_cache: bool):
    """Scrape detailed data for all characters."""
    cache_dir = Path("data/raw")

    # First, get the list of all characters
    console.print("[bold yellow]Step 1: Getting character list...[/bold yellow]")
    list_scraper = CharacterScraper(
        "https://boarhat.gg/games/duet-night-abyss/character/",
        Path("data/processed"),
        cache_dir,
    )
    characters, _ = list_scraper.run()

    console.print(f"\n[bold green]Found {len(characters)} characters[/bold green]\n")

    # Scrape details for each character
    console.print(
        "[bold yellow]Step 2: Scraping detailed data for each character...[/bold yellow]\n"
    )

    success_count = 0
    failed = []

    for i, char in enumerate(characters, 1):
        # Extract slug from URL
        slug = char.url.rstrip("/").split("/")[-1]

        try:
            console.print(f"[{i}/{len(characters)}] Scraping {char.name} ({slug})...")

            if no_cache:
                cache_file = cache_dir / f"character_{slug}.html"
                if cache_file.exists():
                    cache_file.unlink()

            url = f"https://boarhat.gg/games/duet-night-abyss/character/{slug}/"
            scraper = CharacterDetailScraper(url, output_dir, cache_dir, slug)
            data, _ = scraper.run()

            if data:
                success_count += 1
                console.print("  [green]✓ Success[/green]")
            else:
                failed.append(char.name)
                console.print("  [red]✗ No data[/red]")

        except Exception as e:
            failed.append(char.name)
            console.print(f"  [red]✗ Error: {e}[/red]")

    # Summary
    console.print("\n[bold green]Summary[/bold green]")
    console.print(f"  Total: {len(characters)}")
    console.print(f"  Success: {success_count}")
    console.print(f"  Failed: {len(failed)}")

    if failed:
        console.print("\n[yellow]Failed characters:[/yellow]")
        for name in failed:
            console.print(f"  - {name}")

    console.print(f"\n✓ All character details saved to: [bold green]{output_dir}[/bold green]")


@character.command()
@click.argument("character_slug")
@click.option(
    "--output",
    "-o",
    "output_dir",
    type=click.Path(path_type=Path),
    default=Path("data/processed/characters"),
    help="Output directory",
)
@click.option(
    "--no-cache",
    is_flag=True,
    help="Force fetch from URL (ignore cache)",
)
def get(character_slug: str, output_dir: Path, no_cache: bool):
    """Scrape detailed data for a specific character."""
    cache_dir = Path("data/raw")

    # Clear cache if requested
    if no_cache:
        cache_file = cache_dir / f"character_{character_slug}.html"
        if cache_file.exists():
            cache_file.unlink()
            console.print(f"[yellow]Cleared cache: {cache_file}[/yellow]")

    url = f"https://boarhat.gg/games/duet-night-abyss/character/{character_slug}/"
    scraper = CharacterDetailScraper(url, output_dir, cache_dir, character_slug)
    data, output_path = scraper.run()

    if data:
        char = data[0]
        console.print(f"\n[bold green]✓ Scraped details for {char.name}[/bold green]")
        console.print(f"  Profile: {bool(char.profile)}")
        console.print(f"  Traits: {len(char.traits)}")
        console.print(f"  Base Stats: {len(char.base_stats)}")
        console.print(f"  Skills: {len(char.skills)}")

    console.print(f"\n✓ Data saved to: [bold green]{output_path}[/bold green]")


@cli.group()
def weapon():
    """Weapon data commands."""
    pass


@weapon.command("list")
@click.option(
    "--source",
    "-s",
    default="https://boarhat.gg/games/duet-night-abyss/weapon/",
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
def weapon_list(source: str, output_dir: Path, no_cache: bool):
    """Scrape weapon list from boarhat.gg."""
    cache_dir = Path("data/raw")

    # Clear cache if requested
    if no_cache and isinstance(source, str) and source.startswith("http"):
        cache_file = cache_dir / "weapons.html"
        if cache_file.exists():
            cache_file.unlink()
            console.print(f"[yellow]Cleared cache: {cache_file}[/yellow]")

    scraper = WeaponScraper(source, output_dir, cache_dir)
    data, output_path = scraper.run()

    # Display summary
    table = Table(title="Weapon Summary")
    table.add_column("Attribute", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Weapons", str(len(data)))

    # Count by weapon type
    from collections import Counter

    weapon_types = Counter(w.weapon_type for w in data)
    table.add_row("Weapon Types", ", ".join(f"{k}: {v}" for k, v in weapon_types.most_common()))

    # Count by element
    elements = Counter(w.element for w in data)
    table.add_row("Elements", ", ".join(f"{k}: {v}" for k, v in elements.most_common()))

    # Count by attack type
    attack_types = Counter(w.attack_type for w in data)
    table.add_row("Attack Types", ", ".join(f"{k}: {v}" for k, v in attack_types.most_common()))

    console.print(table)
    console.print(f"\n✓ Data saved to: [bold green]{output_path}[/bold green]")


@cli.group()
def geniemon():
    """Geniemon data commands."""
    pass


@geniemon.command("list")
@click.option(
    "--source",
    "-s",
    default="https://boarhat.gg/games/duet-night-abyss/geniemon/",
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
def geniemon_list(source: str, output_dir: Path, no_cache: bool):
    """Scrape geniemon list from boarhat.gg."""
    cache_dir = Path("data/raw")

    # Clear cache if requested
    if no_cache and isinstance(source, str) and source.startswith("http"):
        cache_file = cache_dir / "geniemon.html"
        if cache_file.exists():
            cache_file.unlink()
            console.print(f"[yellow]Cleared cache: {cache_file}[/yellow]")

    scraper = GeniemonScraper(source, output_dir, cache_dir)
    data, output_path = scraper.run()

    # Display summary
    table = Table(title="Geniemon Summary")
    table.add_column("Attribute", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Geniemon", str(len(data)))

    # Count by element
    from collections import Counter

    elements = Counter(g.element for g in data)
    table.add_row("Elements", ", ".join(f"{k}: {v}" for k, v in elements.most_common()))

    # Count by type
    types = Counter(g.geniemon_type for g in data)
    table.add_row("Types", ", ".join(f"{k}: {v}" for k, v in types.most_common()))

    # Count by rarity
    rarities = Counter(g.rarity for g in data)
    table.add_row("Rarities", ", ".join(f"{k}: {v}" for k, v in rarities.most_common()))

    console.print(table)
    console.print(f"\n✓ Data saved to: [bold green]{output_path}[/bold green]")


@cli.command("list")
def list_command():
    """List available scrapers."""
    table = Table(title="Available Scrapers")
    table.add_column("Command", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Status", style="yellow")

    table.add_row("character list", "List all characters", "✓ Available")
    table.add_row("character all", "Scrape all character details", "✓ Available")
    table.add_row("character get [name]", "Scrape specific character", "✓ Available")
    table.add_row("weapon list", "Scrape weapon data", "✓ Available")
    table.add_row("geniemon list", "Scrape geniemon data", "✓ Available")
    table.add_row("demon-wedge", "Scrape demon wedge data", "⚠ Coming soon")

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
