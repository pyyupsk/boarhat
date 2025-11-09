"""Character data model."""

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class CharacterTier:
    """Character tier information."""

    farming: str = "TBD"
    boss: str = "TBD"


@dataclass
class Character:
    """Duet Night Abyss character data model."""

    name: str
    element: Literal["Pyro", "Anemo", "Hydro", "Lumino", "Electro", "Umbro", "Unknown"]
    role: Literal["DPS", "Support", "Unknown"]
    rarity: Literal["SSR", "SR", "R", "Unknown"]
    proficiency: list[str] = field(default_factory=list)
    features: list[str] = field(default_factory=list)
    tier: CharacterTier = field(default_factory=CharacterTier)
    image_url: str = ""
    url: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "element": self.element,
            "role": self.role,
            "rarity": self.rarity,
            "proficiency": self.proficiency,
            "features": self.features,
            "tier": {"farming": self.tier.farming, "boss": self.tier.boss},
            "image_url": self.image_url,
            "url": self.url,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Character":
        """Create from dictionary."""
        tier_data = data.get("tier", {})
        tier = CharacterTier(
            farming=tier_data.get("farming", "TBD"),
            boss=tier_data.get("boss", "TBD"),
        )
        return cls(
            name=data["name"],
            element=data.get("element", "Unknown"),
            role=data.get("role", "Unknown"),
            rarity=data.get("rarity", "Unknown"),
            proficiency=data.get("proficiency", []),
            features=data.get("features", []),
            tier=tier,
            image_url=data.get("image_url", ""),
            url=data.get("url", ""),
        )
