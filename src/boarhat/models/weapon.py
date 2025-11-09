"""Weapon data model."""

from dataclasses import dataclass, field


@dataclass
class Weapon:
    """Duet Night Abyss weapon data model."""

    name: str
    weapon_type: str
    rarity: str = "Unknown"
    image_url: str = ""
    url: str = ""
    stats: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "weapon_type": self.weapon_type,
            "rarity": self.rarity,
            "image_url": self.image_url,
            "url": self.url,
            "stats": self.stats,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Weapon":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            weapon_type=data.get("weapon_type", "Unknown"),
            rarity=data.get("rarity", "Unknown"),
            image_url=data.get("image_url", ""),
            url=data.get("url", ""),
            stats=data.get("stats", {}),
        )
