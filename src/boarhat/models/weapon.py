"""Weapon data model."""

from dataclasses import dataclass, field


@dataclass
class Weapon:
    """Duet Night Abyss weapon data model."""

    name: str
    element: str
    weapon_type: str
    attack_type: str
    image_url: str = ""
    skill: str = ""
    base_stats: dict = field(default_factory=dict)
    attributes: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "element": self.element,
            "weapon_type": self.weapon_type,
            "attack_type": self.attack_type,
            "image_url": self.image_url,
            "skill": self.skill,
            "base_stats": self.base_stats,
            "attributes": self.attributes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Weapon":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            element=data.get("element", "Neutral"),
            weapon_type=data.get("weapon_type", "Unknown"),
            attack_type=data.get("attack_type", "Unknown"),
            image_url=data.get("image_url", ""),
            skill=data.get("skill", ""),
            base_stats=data.get("base_stats", {}),
            attributes=data.get("attributes", {}),
        )
