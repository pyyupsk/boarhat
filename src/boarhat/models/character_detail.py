"""Extended character data model for detail pages."""

from dataclasses import dataclass, field


@dataclass
class Profile:
    """Character profile information."""

    gender: str = ""
    birthplace: str = ""
    birthday: str = ""
    allegiance: str = ""


@dataclass
class Trait:
    """Character trait."""

    name: str
    effect: str


@dataclass
class BaseStat:
    """Base stat information."""

    stat: str
    level_1: str
    level_max: str


@dataclass
class Skill:
    """Skill information."""

    name: str
    type: str  # "Skill - DMG", "Ultimate - Buff", etc.
    description: str
    stats: dict[str, dict[str, str]] = field(default_factory=dict)  # stat_name -> {level_1, level_max}


@dataclass
class CharacterDetail:
    """Detailed character information from individual character pages."""

    name: str
    slug: str  # URL slug (e.g., "berenica")
    url: str
    image_url: str = ""
    profile: Profile | None = None
    traits: list[Trait] = field(default_factory=list)
    base_stats: list[BaseStat] = field(default_factory=list)
    skills: list[Skill] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "slug": self.slug,
            "url": self.url,
            "image_url": self.image_url,
            "profile": {
                "gender": self.profile.gender if self.profile else "",
                "birthplace": self.profile.birthplace if self.profile else "",
                "birthday": self.profile.birthday if self.profile else "",
                "allegiance": self.profile.allegiance if self.profile else "",
            }
            if self.profile
            else None,
            "traits": [{"name": t.name, "effect": t.effect} for t in self.traits],
            "base_stats": [
                {"stat": s.stat, "level_1": s.level_1, "level_max": s.level_max}
                for s in self.base_stats
            ],
            "skills": [
                {
                    "name": s.name,
                    "type": s.type,
                    "description": s.description,
                    "stats": s.stats,
                }
                for s in self.skills
            ],
        }
