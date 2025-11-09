"""Character scraper."""

from boarhat.models import Character, CharacterTier
from boarhat.scrapers.base import BaseScraper


class CharacterScraper(BaseScraper[Character]):
    """Scraper for character data."""

    @property
    def category_name(self) -> str:
        """Category name."""
        return "characters"

    def _parse_rarity(self, border_class: str) -> str:
        """Parse rarity from border color class."""
        rarity_map = {
            "border-red-400": "SSR",
            "border-green-400": "SR",
            "border-blue-400": "R",
        }
        for color, rarity in rarity_map.items():
            if color in border_class:
                return rarity
        return "Unknown"

    def scrape(self) -> list[Character]:
        """Scrape character data."""
        soup = self.load_html()
        characters = []

        # Find all character cards
        character_cards = soup.find_all("a", href=lambda x: x and "/character/" in x)

        for card in character_cards:
            try:
                # Extract character URL
                url = card.get("href", "")
                if not url or url.endswith("/character/"):
                    continue

                # Get character name
                name_elem = card.find("div", class_="text-sm")
                if not name_elem:
                    continue
                name = name_elem.get_text(strip=True)

                # Extract rarity from border color
                border_div = card.find("div", class_=lambda x: x and "border-" in x)
                rarity = "Unknown"
                if border_div:
                    classes = border_div.get("class", [])
                    rarity = self._parse_rarity(" ".join(classes))

                # Extract element and role
                element_role_divs = card.find_all("div", class_="text-xs text-gray-400 text-center")
                element = "Unknown"
                role = "Unknown"

                for div in element_role_divs[:1]:
                    text = div.get_text(strip=True).replace("<!-- -->", "")
                    parts = [p.strip() for p in text.split("|")]
                    if len(parts) >= 2:
                        element = parts[0]
                        role = parts[1]
                    break

                # Extract image URL
                img = card.find("img")
                image_url = img.get("src", "") if img else ""

                # Find the hover tooltip for additional details
                tooltip = card.find("div", class_=lambda x: x and "group-hover:flex" in x)
                proficiency = []
                features = []
                tier = CharacterTier()

                if tooltip:
                    # Extract proficiency
                    prof_elem = tooltip.find("strong", string="Proficiency:")
                    if prof_elem and prof_elem.parent:
                        prof_text = prof_elem.parent.get_text(strip=True)
                        prof_text = prof_text.replace("Proficiency:", "").strip()
                        proficiency = [p.strip() for p in prof_text.split(",")]

                    # Extract features
                    feat_elem = tooltip.find("strong", string="Feature:")
                    if feat_elem and feat_elem.parent:
                        feat_text = feat_elem.parent.get_text(strip=True)
                        feat_text = feat_text.replace("Feature:", "").strip()
                        features = [f.strip() for f in feat_text.split(",")]

                    # Extract tier information
                    tier_grid = tooltip.find("div", class_="grid-cols-2")
                    if tier_grid:
                        tier_items = tier_grid.find_all("div", class_="flex-col")
                        for item in tier_items:
                            label = item.find("span", class_="font-bold text-white")
                            value = item.find("span", class_=lambda x: x and "bg-" in x)

                            if label and value:
                                label_text = label.get_text(strip=True)
                                value_text = value.get_text(strip=True)

                                if "Farming" in label_text:
                                    tier.farming = value_text.strip()
                                elif "Boss" in label_text:
                                    tier.boss = value_text.strip()

                character = Character(
                    name=name,
                    element=element,  # type: ignore
                    role=role,  # type: ignore
                    rarity=rarity,  # type: ignore
                    proficiency=proficiency,
                    features=features,
                    tier=tier,
                    image_url=image_url,
                    url=f"https://boarhat.gg{url}",
                )

                characters.append(character)

            except Exception as e:
                print(f"Error parsing character card: {e}")
                continue

        return characters
