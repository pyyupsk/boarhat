# Boarhat

Comprehensive data scraper for [Duet Night Abyss](https://boarhat.gg/games/duet-night-abyss/) from boarhat.gg.

## Installation

```bash
uv sync
```

## Usage

```bash
# Scrape characters
uv run boarhat characters

# List available scrapers
uv run boarhat list-scrapers

# Force refresh cache
uv run boarhat characters --no-cache
```

## Available Scrapers

| Command       | Status         |
| ------------- | -------------- |
| `characters`  | ✅ Available   |
| `weapons`     | 🚧 Coming soon |
| `geniemon`    | 🚧 Coming soon |
| `demon-wedge` | 🚧 Coming soon |

## Structure

```text
boarhat/
├── src/boarhat/
│   ├── cli.py           # CLI interface
│   ├── models/          # Data models
│   └── scrapers/        # Scraper implementations
└── data/
    ├── raw/             # Cached HTML
    └── processed/       # JSON output
```

## Adding a New Scraper

1. Create model in `src/boarhat/models/`
2. Create scraper extending `BaseScraper` in `src/boarhat/scrapers/`
3. Add CLI command in `src/boarhat/cli.py`

## License

Educational and research purposes only. All game data belongs to respective owners.
