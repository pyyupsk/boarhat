"""Weapon list scraper for Duet Night Abyss."""

from boarhat.models.weapon import Weapon
from boarhat.scrapers.base import BaseScraper


class WeaponScraper(BaseScraper[Weapon]):
    """Scraper for weapon list from boarhat.gg."""

    @property
    def category_name(self) -> str:
        """Category name for weapon scraper."""
        return "weapons"

    def scrape(self) -> list[Weapon]:
        """
        Scrape weapon data from the HTML.

        Returns:
            List of Weapon objects
        """
        soup = self.load_html()
        weapons = []

        # Find all weapon name headings (h2 with specific class)
        weapon_headings = soup.find_all("h2", class_="text-xl font-bold text-white")

        for heading in weapon_headings:
            # Skip headings that are not weapon names
            heading_text = heading.get_text(strip=True)
            if heading_text in ["WEAPON", "Element", "Type", "Attack Type"]:
                continue

            try:
                # Find the parent card div
                card = heading.find_parent("div", class_="bg-gray-900")
                if not card:
                    continue

                weapon = self._parse_weapon_card(heading_text, card)
                if weapon:
                    weapons.append(weapon)
            except Exception as e:
                print(f"Warning: Failed to parse weapon '{heading_text}': {e}")
                continue

        return weapons

    def _parse_weapon_card(self, name: str, card) -> Weapon | None:
        """
        Parse a single weapon card.

        Args:
            name: Weapon name
            card: BeautifulSoup element containing weapon card

        Returns:
            Weapon object or None if parsing fails
        """
        # Extract metadata from span tags
        element = "Neutral"
        weapon_type = "Unknown"
        attack_type = "Unknown"

        # Find all badge spans
        badges = card.find_all("span", class_=lambda c: c and "px-2" in c and "py-1" in c)

        for badge in badges:
            text = badge.get_text(strip=True)
            bg_class = badge.get("class", [])
            bg_color = " ".join(bg_class)

            # Weapon type is the one with bg-gray-700
            if "bg-gray-700" in bg_color:
                weapon_type = text
            else:
                # Check if it's an element or attack type
                elements = ["Pyro", "Anemo", "Hydro", "Lumino", "Electro", "Umbro", "Neutral"]
                attack_types = ["Slash", "Spike", "Smash"]

                if text in elements:
                    element = text
                elif text in attack_types:
                    attack_type = text

        # Extract image URL from the background-image style
        image_url = ""
        # Look for div with background-image style
        img_divs = card.find_all("div", style=lambda s: s and "background-image:url(" in str(s))
        for img_div in img_divs:
            style = img_div.get("style", "")
            if "background-image:url(" in style:
                start_idx = style.find("background-image:url(") + len("background-image:url(")
                end_idx = style.find(")", start_idx)
                image_url = style[start_idx:end_idx]
                # Make absolute URL if needed
                if image_url.startswith("/"):
                    image_url = f"https://boarhat.gg{image_url}"
                break

        # Extract skill description
        skill = ""
        skill_heading = card.find("h3", string="Skill")
        if skill_heading:
            # Get the parent div containing the skill text
            skill_div = skill_heading.find_parent("div")
            if skill_div:
                # Get all text from the div and remove the "Skill" heading
                full_text = skill_div.get_text(separator=" ", strip=True)
                if "Skill" in full_text:
                    skill = full_text.replace("Skill", "", 1).strip()

        # Extract base stats
        base_stats = {}
        stats_heading = card.find("h3", string=lambda t: t and "Stats" in str(t))
        if stats_heading:
            stats_list = stats_heading.find_next("ul")
            if stats_list:
                for li in stats_list.find_all("li"):
                    text = li.get_text(separator=" ", strip=True)
                    # Parse "Key: Value" format
                    if ":" in text:
                        parts = text.split(":", 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip()
                            # Normalize key
                            stat_key = key.lower().replace(" ", "_").replace("-", "_")
                            base_stats[stat_key] = value

        # Extract attributes
        attributes = {}
        attr_heading = card.find("h3", string="Attributes")
        if attr_heading:
            attr_list = attr_heading.find_next("ul")
            if attr_list:
                for li in attr_list.find_all("li"):
                    text = li.get_text(separator=" ", strip=True)
                    if ":" in text:
                        parts = text.split(":", 1)
                        if len(parts) == 2:
                            key = parts[0].strip()
                            value = parts[1].strip()
                            attr_key = key.lower().replace(" ", "_").replace("-", "_")
                            attributes[attr_key] = value

        return Weapon(
            name=name,
            element=element,
            weapon_type=weapon_type,
            attack_type=attack_type,
            image_url=image_url,
            skill=skill,
            base_stats=base_stats,
            attributes=attributes,
        )
