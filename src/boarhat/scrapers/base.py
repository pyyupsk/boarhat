"""Base scraper class."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, TypeVar

import httpx
from bs4 import BeautifulSoup

T = TypeVar("T")


class BaseScraper(ABC, Generic[T]):
    """Base class for all scrapers."""

    def __init__(
        self,
        source: str | Path,
        output_dir: Path,
        cache_dir: Path | None = None,
    ):
        """
        Initialize the scraper.

        Args:
            source: URL or Path to HTML file to scrape
            output_dir: Directory to save output files
            cache_dir: Optional directory to cache downloaded HTML
        """
        self.source = source
        self.output_dir = output_dir
        self.cache_dir = cache_dir or Path("data/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @property
    @abstractmethod
    def category_name(self) -> str:
        """Category name for this scraper (e.g., 'character', 'weapon')."""
        pass

    @abstractmethod
    def scrape(self) -> list[T]:
        """
        Scrape data from the HTML file.

        Returns:
            List of scraped data objects
        """
        pass

    def load_html(self) -> BeautifulSoup:
        """Load and parse HTML from source (URL or file)."""
        html_content = ""

        # Check if source is a URL
        if isinstance(self.source, str) and self.source.startswith("http"):
            # Check cache first
            cache_file = self.cache_dir / f"{self.category_name}.html"

            if cache_file.exists():
                print(f"[{self.category_name}] Loading from cache: {cache_file}")
                with open(cache_file, "r", encoding="utf-8") as f:
                    html_content = f.read()
            else:
                print(f"[{self.category_name}] Fetching from URL: {self.source}")
                response = httpx.get(self.source, follow_redirects=True, timeout=30.0)
                response.raise_for_status()
                html_content = response.text

                # Cache the response
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"[{self.category_name}] Cached to: {cache_file}")
        else:
            # Load from file
            file_path = Path(self.source)
            if not file_path.exists():
                raise FileNotFoundError(f"HTML file not found: {file_path}")

            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()

        return BeautifulSoup(html_content, "lxml")

    def save_json(self, data: list[dict[str, Any]], filename: str | None = None) -> Path:
        """
        Save data to JSON file.

        Args:
            data: List of dictionaries to save
            filename: Optional filename (defaults to category_name.json)

        Returns:
            Path to the saved file
        """
        if filename is None:
            filename = f"{self.category_name}.json"

        output_file = self.output_dir / filename

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return output_file

    def run(self) -> tuple[list[T], Path]:
        """
        Run the scraper and save results.

        Returns:
            Tuple of (scraped data, output file path)
        """
        print(f"[{self.category_name}] Scraping from {self.source}...")
        data = self.scrape()

        print(f"[{self.category_name}] Found {len(data)} items")

        # Convert to dict if objects have to_dict method
        dict_data = []
        for item in data:
            if hasattr(item, "to_dict"):
                dict_data.append(item.to_dict())
            elif isinstance(item, dict):
                dict_data.append(item)
            else:
                dict_data.append(item.__dict__)

        output_path = self.save_json(dict_data)
        print(f"[{self.category_name}] Saved to {output_path}")

        return data, output_path
