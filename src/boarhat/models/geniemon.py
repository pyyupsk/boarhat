"""Geniemon data model."""

from dataclasses import dataclass, field


@dataclass
class Geniemon:
    """Duet Night Abyss geniemon data model."""

    name: str
    element: str
    geniemon_type: str  # Active or Inactive
    rarity: str  # 5★, 4★, 3★, 2★
    image_url: str = ""
    active_skill: str = ""
    cooldown: str = ""
    passive_skill: str = ""
    ascensions: list[str] = field(default_factory=list)
    location: str = ""
    lore: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "element": self.element,
            "geniemon_type": self.geniemon_type,
            "rarity": self.rarity,
            "image_url": self.image_url,
            "active_skill": self.active_skill,
            "cooldown": self.cooldown,
            "passive_skill": self.passive_skill,
            "ascensions": self.ascensions,
            "location": self.location,
            "lore": self.lore,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Geniemon":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            element=data.get("element", "Neutral"),
            geniemon_type=data.get("geniemon_type", "Unknown"),
            rarity=data.get("rarity", "Unknown"),
            image_url=data.get("image_url", ""),
            active_skill=data.get("active_skill", ""),
            cooldown=data.get("cooldown", ""),
            passive_skill=data.get("passive_skill", ""),
            ascensions=data.get("ascensions", []),
            location=data.get("location", ""),
            lore=data.get("lore", ""),
        )
