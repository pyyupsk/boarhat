"""Scrapers for different data categories."""

from .base import BaseScraper
from .character import CharacterScraper
from .geniemon import GeniemonScraper
from .weapon import WeaponScraper

__all__ = ["BaseScraper", "CharacterScraper", "GeniemonScraper", "WeaponScraper"]
