"""Character detail page scraper."""

from pathlib import Path

from boarhat.models.character_detail import BaseStat, CharacterDetail, Profile, Skill, Trait
from boarhat.scrapers.base import BaseScraper


class CharacterDetailScraper(BaseScraper[CharacterDetail]):
    """Scraper for individual character detail pages."""

    def __init__(
        self,
        source: str | Path,
        output_dir: Path,
        cache_dir: Path | None = None,
        character_slug: str | None = None,
    ):
        """
        Initialize the character detail scraper.

        Args:
            source: URL or Path to HTML file
            output_dir: Directory to save output files
            cache_dir: Optional cache directory
            character_slug: Character slug (e.g., "berenica") for caching
        """
        super().__init__(source, output_dir, cache_dir)
        self.character_slug = character_slug

    @property
    def category_name(self) -> str:
        """Category name."""
        if self.character_slug:
            return f"character_{self.character_slug}"
        return "character_detail"

    def _parse_profile(self, soup) -> Profile | None:
        """Parse profile table."""
        profile_tables = soup.find_all("table", class_="table-auto")

        for table in profile_tables:
            rows = table.find_all("tr")
            profile_data = {}

            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True).lower()
                    value = cols[1].get_text(strip=True)
                    profile_data[key] = value

            if "gender" in profile_data:
                return Profile(
                    gender=profile_data.get("gender", ""),
                    birthplace=profile_data.get("birthplace", ""),
                    birthday=profile_data.get("birthday", ""),
                    allegiance=profile_data.get("allegiance", ""),
                )

        return None

    def _parse_traits(self, soup) -> list[Trait]:
        """Parse traits table."""
        traits = []

        # Find trait table (has NAME and EFFECT headers)
        tables = soup.find_all("table", class_="table-auto")

        for table in tables:
            headers = table.find_all("th")
            if len(headers) >= 2:
                header_text = [h.get_text(strip=True) for h in headers]
                if "NAME" in header_text and "EFFECT" in header_text:
                    rows = table.find("tbody").find_all("tr") if table.find("tbody") else []

                    for row in rows:
                        cols = row.find_all("td")
                        if len(cols) >= 2:
                            name = cols[0].get_text(strip=True)
                            effect = " ".join(cols[1].get_text().split())
                            traits.append(Trait(name=name, effect=effect))

        return traits

    def _parse_base_stats(self, soup) -> list[BaseStat]:
        """Parse base stats table."""
        stats = []

        # Find base stats section
        base_stats_header = soup.find("h2", id="base-stats")
        if base_stats_header:
            # Find the next table
            table = base_stats_header.find_next("table", class_="table-auto")
            if table:
                rows = table.find("tbody").find_all("tr") if table.find("tbody") else []

                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) == 3:
                        stat = cols[0].get_text(strip=True)
                        level_1 = cols[1].get_text(strip=True)
                        level_max = cols[2].get_text(strip=True)
                        stats.append(BaseStat(stat=stat, level_1=level_1, level_max=level_max))
                    elif len(cols) == 2 and cols[0].get("colspan"):
                        # Handle colspan cells (like Feature, Weapon Proficiency)
                        stat = cols[0].get_text(strip=True)
                        value = cols[1].get_text(strip=True) if len(cols) > 1 else ""
                        stats.append(BaseStat(stat=stat, level_1=value, level_max=value))

        return stats

    def _parse_skills(self, soup) -> list[Skill]:
        """Parse skills section."""
        skills = []

        # Find skills section
        skill_header = soup.find("h2", id="skill")
        if skill_header:
            # Find all skill containers
            skill_containers = skill_header.find_next("div", class_="grid").find_all(
                "div", recursive=False
            )

            for container in skill_containers:
                skill_type_elem = container.find("b", class_="bg-gray-800")
                if not skill_type_elem:
                    continue

                skill_type = skill_type_elem.get_text(strip=True)
                skill_name_elem = container.find("b", class_="font-bold")
                if not skill_name_elem or skill_name_elem == skill_type_elem:
                    skill_name_elems = container.find_all("b", class_="font-bold")
                    skill_name_elem = skill_name_elems[1] if len(skill_name_elems) > 1 else None

                skill_name = skill_name_elem.get_text(strip=True) if skill_name_elem else "Unknown"

                # Get description and clean whitespace
                desc_elem = container.find("p", class_="text-white")
                description = " ".join(desc_elem.get_text().split()) if desc_elem else ""

                # Parse stats table
                stat_table = container.find("table")
                stats_dict = {}

                if stat_table:
                    rows = (
                        stat_table.find("tbody").find_all("tr") if stat_table.find("tbody") else []
                    )

                    for row in rows:
                        cols = row.find_all("td")
                        if len(cols) == 3:
                            stat_name = cols[0].get_text(strip=True)
                            level_1 = cols[1].get_text(strip=True)
                            level_max = cols[2].get_text(strip=True)
                            stats_dict[stat_name] = {"level_1": level_1, "level_max": level_max}

                skills.append(
                    Skill(
                        name=skill_name,
                        type=skill_type,
                        description=description,
                        stats=stats_dict,
                    )
                )

        return skills

    def scrape(self) -> list[CharacterDetail]:
        """Scrape character detail data."""
        soup = self.load_html()

        # Get character name from title or header
        title = soup.find("title")
        name = "Unknown"
        if title:
            name = title.get_text(strip=True).split("|")[0].strip()

        # Get character slug from URL or source
        slug = self.character_slug or "unknown"
        if isinstance(self.source, str) and "character/" in self.source:
            slug = self.source.rstrip("/").split("/")[-1]

        # Get main character image
        image_url = ""
        main_image = soup.find("img", alt=name)
        if main_image and main_image.get("src"):
            image_url = str(main_image.get("src", ""))

        # Parse sections
        profile = self._parse_profile(soup)
        traits = self._parse_traits(soup)
        base_stats = self._parse_base_stats(soup)
        skills = self._parse_skills(soup)

        character_detail = CharacterDetail(
            name=name,
            slug=slug,
            url=self.source if isinstance(self.source, str) else "",
            image_url=image_url,
            profile=profile,
            traits=traits,
            base_stats=base_stats,
            skills=skills,
        )

        return [character_detail]

    def save_json(self, data: list[dict], filename: str | None = None) -> Path:
        """Override to save individual character file."""
        if filename is None and self.character_slug:
            filename = f"{self.character_slug}_detail.json"
        return super().save_json(data, filename)
