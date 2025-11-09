"""Demon Wedge list scraper for Duet Night Abyss."""

from boarhat.models.demon_wedge import DemonWedge
from boarhat.scrapers.base import BaseScraper


class DemonWedgeScraper(BaseScraper[DemonWedge]):
    """Scraper for demon wedge list from boarhat.gg."""

    @property
    def category_name(self) -> str:
        """Category name for demon wedge scraper."""
        return "demon_wedges"

    def scrape(self) -> list[DemonWedge]:
        """
        Scrape demon wedge data from the HTML.

        Returns:
            List of DemonWedge objects
        """
        soup = self.load_html()
        wedges = []

        # Find all demon wedge name headings (h2 with specific class)
        wedge_headings = soup.find_all("h2", class_="text-xl font-bold text-white")

        for heading in wedge_headings:
            # Skip headings that are not wedge names
            heading_text = heading.get_text(strip=True)
            if heading_text in ["DEMON WEDGE", "Polarity", "Restriction", "Source", "Rarity"]:
                continue

            try:
                # Find the parent card div
                card = heading.find_parent("div", class_="bg-gray-900")
                if not card:
                    continue

                # Get subtype from the <p> tag after the heading
                subtype = "Unknown"
                subtype_p = heading.find_next_sibling("p")
                if subtype_p:
                    subtype = subtype_p.get_text(strip=True)

                wedge = self._parse_wedge_card(heading_text, subtype, card)
                if wedge:
                    wedges.append(wedge)
            except Exception as e:
                print(f"Warning: Failed to parse demon wedge '{heading_text}': {e}")
                continue

        return wedges

    def _parse_wedge_card(self, name: str, subtype: str, card) -> DemonWedge | None:
        """
        Parse a single demon wedge card.

        Args:
            name: Demon wedge name
            subtype: Demon wedge subtype (Volition, Spectrum, etc.)
            card: BeautifulSoup element containing wedge card

        Returns:
            DemonWedge object or None if parsing fails
        """
        # Extract metadata from span tags
        rarity = "Unknown"
        restriction = "Unknown"
        element = "Unknown"
        polarity = ""

        # Find all badge spans
        badges = card.find_all("span", class_=lambda c: c and "px-2" in c and "py-1" in c)

        for badge in badges:
            text = badge.get_text(strip=True)
            bg_class = badge.get("class", [])
            bg_color = " ".join(bg_class)

            # Rarity has star symbol
            if "★" in text:
                rarity = text
            # Restriction/Type (bg-gray-700)
            elif "bg-gray-700" in bg_color:
                restriction = text
            # Polarity has special symbols (has title="Polarity")
            elif badge.get("title") == "Polarity":
                polarity = text
            else:
                # Check if it's an element
                elements = ["Pyro", "Anemo", "Hydro", "Lumino", "Electro", "Umbro"]
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

        # Extract main attributes
        main_attributes = []
        attr_heading = card.find("h3", string="Main Attribute")
        if attr_heading:
            attr_list = attr_heading.find_next("ul")
            if attr_list:
                for li in attr_list.find_all("li"):
                    text = li.get_text(strip=True)
                    if text:
                        main_attributes.append(text)

        # Extract effects
        effects = []
        effect_heading = card.find("h3", string="Effect")
        if effect_heading:
            effect_list = effect_heading.find_next("ul")
            if effect_list:
                for li in effect_list.find_all("li"):
                    text = li.get_text(strip=True)
                    if text:
                        effects.append(text)

        # Extract tolerance, track, and source
        tolerance = ""
        track = ""
        source = ""

        # Find the div with gray text at the bottom
        info_div = card.find(
            "div", class_=lambda c: c and "text-gray-400" in str(c) and "text-xs" in str(c)
        )
        if info_div:
            for p in info_div.find_all("p"):
                text = p.get_text(strip=True)
                if text.startswith("Tolerance:"):
                    tolerance = text.replace("Tolerance:", "").strip()
                elif text.startswith("Track:"):
                    track = text.replace("Track:", "").strip()
                elif text.startswith("Source:"):
                    source = text.replace("Source:", "").strip()

        return DemonWedge(
            name=name,
            subtype=subtype,
            rarity=rarity,
            restriction=restriction,
            element=element,
            polarity=polarity,
            image_url=image_url,
            main_attributes=main_attributes,
            effects=effects,
            tolerance=tolerance,
            track=track,
            source=source,
        )
