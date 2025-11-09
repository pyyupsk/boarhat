"""Scrapers for different data categories."""

from .base import BaseScraper
from .character import CharacterScraper
from .weapon import WeaponScraper

__all__ = ["BaseScraper", "CharacterScraper", "WeaponScraper"]
