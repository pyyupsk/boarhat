"""Scrapers for different data categories."""

from .base import BaseScraper
from .character import CharacterScraper
from .demon_wedge import DemonWedgeScraper
from .geniemon import GeniemonScraper
from .weapon import WeaponScraper

__all__ = [
    "BaseScraper",
    "CharacterScraper",
    "DemonWedgeScraper",
    "GeniemonScraper",
    "WeaponScraper",
]
