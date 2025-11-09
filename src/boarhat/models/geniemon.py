"""Geniemon data model."""

from dataclasses import dataclass, field


@dataclass
class Geniemon:
    """Duet Night Abyss geniemon data model."""

    name: str
    rarity: str = "Unknown"
    image_url: str = ""
    url: str = ""
    abilities: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "rarity": self.rarity,
            "image_url": self.image_url,
            "url": self.url,
            "abilities": self.abilities,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Geniemon":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            rarity=data.get("rarity", "Unknown"),
            image_url=data.get("image_url", ""),
            url=data.get("url", ""),
            abilities=data.get("abilities", []),
        )
