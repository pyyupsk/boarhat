"""Geniemon list scraper for Duet Night Abyss."""

from boarhat.models.geniemon import Geniemon
from boarhat.scrapers.base import BaseScraper


class GeniemonScraper(BaseScraper[Geniemon]):
    """Scraper for geniemon list from boarhat.gg."""

    @property
    def category_name(self) -> str:
        """Category name for geniemon scraper."""
        return "geniemon"

    def scrape(self) -> list[Geniemon]:
        """
        Scrape geniemon data from the HTML.

        Returns:
            List of Geniemon objects
        """
        soup = self.load_html()
        geniemons = []

        # Find all geniemon name headings (h2 with specific class)
        geniemon_headings = soup.find_all("h2", class_="text-xl font-bold text-white")

        for heading in geniemon_headings:
            # Skip headings that are not geniemon names
            heading_text = heading.get_text(strip=True)
            if heading_text in ["GENIEMON", "Element", "Type", "Rarity"]:
                continue

            try:
                # Find the parent card div
                card = heading.find_parent("div", class_="bg-gray-900")
                if not card:
                    continue

                geniemon = self._parse_geniemon_card(heading_text, card)
                if geniemon:
                    geniemons.append(geniemon)
            except Exception as e:
                print(f"Warning: Failed to parse geniemon '{heading_text}': {e}")
                continue

        return geniemons

    def _parse_geniemon_card(self, name: str, card) -> Geniemon | None:
        """
        Parse a single geniemon card.

        Args:
            name: Geniemon name
            card: BeautifulSoup element containing geniemon card

        Returns:
            Geniemon object or None if parsing fails
        """
        # Extract metadata from span tags
        element = "Neutral"
        geniemon_type = "Unknown"
        rarity = "Unknown"

        # Find all badge spans
        badges = card.find_all("span", class_=lambda c: c and "px-2" in c and "py-1" in c)

        for badge in badges:
            text = badge.get_text(strip=True)
            bg_class = badge.get("class", [])
            bg_color = " ".join(bg_class)

            # Type is the one with bg-gray-700 (Active/Inactive)
            if "bg-gray-700" in bg_color:
                geniemon_type = text
            # Rarity has star symbol
            elif "★" in text:
                rarity = text
            else:
                # Check if it's an element
                elements = ["Pyro", "Anemo", "Hydro", "Lumino", "Electro", "Umbro", "Neutral"]
                if text in elements:
                    element = text

        # Extract image URL from the background-image style
        image_url = ""
        img_divs = card.find_all("div", style=lambda s: s and "background-image:url(" in str(s))
        for img_div in img_divs:
            style = img_div.get("style", "")
            if "background-image:url(" in style:
                start_idx = style.find("background-image:url(") + len("background-image:url(")
                end_idx = style.find(")", start_idx)
                image_url = style[start_idx:end_idx]
                if image_url.startswith("/"):
                    image_url = f"https://boarhat.gg{image_url}"
                break

        # Extract active skill
        active_skill = ""
        active_heading = card.find("h3", string=lambda t: t and "Active Skill" in str(t))
        if active_heading:
            # Get the next <p> tag after the heading
            skill_p = active_heading.find_next("p")
            if skill_p:
                active_skill = skill_p.get_text(strip=True)

        # Extract cooldown
        cooldown = ""
        cooldown_heading = card.find("h3", string="Cooldown")
        if cooldown_heading:
            cooldown_p = cooldown_heading.find_next("p")
            if cooldown_p:
                cooldown = cooldown_p.get_text(strip=True)

        # Extract passive skill
        passive_skill = ""
        passive_heading = card.find("h3", string=lambda t: t and "Passive Skill" in str(t))
        if passive_heading:
            passive_p = passive_heading.find_next("p")
            if passive_p:
                passive_skill = passive_p.get_text(strip=True)

        # Extract ascensions (Smelt)
        ascensions = []
        smelt_heading = card.find("h3", string="Smelt")
        if smelt_heading:
            smelt_list = smelt_heading.find_next("ul")
            if smelt_list:
                for li in smelt_list.find_all("li"):
                    text = li.get_text(separator=" ", strip=True)
                    ascensions.append(text)

        # Extract location
        location = ""
        location_heading = card.find("h3", string="Location")
        if location_heading:
            location_p = location_heading.find_next("p")
            if location_p:
                location = location_p.get_text(strip=True)

        # Extract lore (the italic text at the bottom)
        lore = ""
        lore_div = card.find("div", class_=lambda c: c and "italic" in str(c))
        if lore_div:
            lore = lore_div.get_text(strip=True)

        return Geniemon(
            name=name,
            element=element,
            geniemon_type=geniemon_type,
            rarity=rarity,
            image_url=image_url,
            active_skill=active_skill,
            cooldown=cooldown,
            passive_skill=passive_skill,
            ascensions=ascensions,
            location=location,
            lore=lore,
        )
