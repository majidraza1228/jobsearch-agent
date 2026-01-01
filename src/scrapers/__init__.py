"""Scrapers package for job search agent."""

from .base_scraper import BaseScraper
from .indeed_scraper import IndeedScraper
from .linkedin_scraper import LinkedinScraper
from .glassdoor_scraper import GlassdoorScraper
from .monster_scraper import MonsterScraper
from .serpapi_scraper import SerpApiScraper
from .adzuna_scraper import AdzunaScraper

__all__ = [
    "BaseScraper",
    "IndeedScraper",
    "LinkedinScraper",
    "GlassdoorScraper",
    "MonsterScraper",
    "SerpApiScraper",
    "AdzunaScraper",
]
