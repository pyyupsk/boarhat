"""Demon Wedge data model."""

from dataclasses import dataclass, field


@dataclass
class DemonWedge:
    """Duet Night Abyss demon wedge data model."""

    name: str
    subtype: str  # Volition, Spectrum, Morale, etc.
    rarity: str  # 5★, 4★, 3★, 2★
    restriction: str  # Characters, Melee Weapon, Ranged Weapon, Consonance Weapon
    element: str  # Pyro, Anemo, Hydro, Lumino, Electro, Umbro
    polarity: str  # ◊, ◬, ☽, ⊙
    image_url: str = ""
    main_attributes: list[str] = field(default_factory=list)
    effects: list[str] = field(default_factory=list)
    tolerance: str = ""
    track: str = ""
    source: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "subtype": self.subtype,
            "rarity": self.rarity,
            "restriction": self.restriction,
            "element": self.element,
            "polarity": self.polarity,
            "image_url": self.image_url,
            "main_attributes": self.main_attributes,
            "effects": self.effects,
            "tolerance": self.tolerance,
            "track": self.track,
            "source": self.source,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DemonWedge":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            subtype=data.get("subtype", "Unknown"),
            rarity=data.get("rarity", "Unknown"),
            restriction=data.get("restriction", "Unknown"),
            element=data.get("element", "Unknown"),
            polarity=data.get("polarity", ""),
            image_url=data.get("image_url", ""),
            main_attributes=data.get("main_attributes", []),
            effects=data.get("effects", []),
            tolerance=data.get("tolerance", ""),
            track=data.get("track", ""),
            source=data.get("source", ""),
        )
