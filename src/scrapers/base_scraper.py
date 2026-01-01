"""Base scraper class for all job scrapers."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Abstract base class for job scrapers."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize scraper with API key."""
        self.api_key = api_key
        self.source_name = self.__class__.__name__.replace("Scraper", "").lower()

    @abstractmethod
    def search_jobs(
        self, keywords: str, location: str = "", **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search for jobs with given parameters.

        Args:
            keywords: Job search keywords
            location: Job location
            **kwargs: Additional search parameters

        Returns:
            List of job dictionaries
        """
        pass

    def normalize_job(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize job data to standard format.

        Args:
            raw_job: Raw job data from API

        Returns:
            Normalized job dictionary
        """
        return {
            "external_id": self._extract_external_id(raw_job),
            "source": self.source_name,
            "title": self._extract_title(raw_job),
            "company": self._extract_company(raw_job),
            "location": self._extract_location(raw_job),
            "description": self._extract_description(raw_job),
            "url": self._extract_url(raw_job),
            "job_type": self._extract_job_type(raw_job),
            "remote_type": self._extract_remote_type(raw_job),
            "salary_min": self._extract_salary_min(raw_job),
            "salary_max": self._extract_salary_max(raw_job),
            "posted_date": self._extract_posted_date(raw_job),
            "raw_data": raw_job,
        }

    @abstractmethod
    def _extract_external_id(self, raw_job: Dict[str, Any]) -> str:
        """Extract unique job ID."""
        pass

    @abstractmethod
    def _extract_title(self, raw_job: Dict[str, Any]) -> str:
        """Extract job title."""
        pass

    @abstractmethod
    def _extract_company(self, raw_job: Dict[str, Any]) -> str:
        """Extract company name."""
        pass

    @abstractmethod
    def _extract_location(self, raw_job: Dict[str, Any]) -> str:
        """Extract job location."""
        pass

    @abstractmethod
    def _extract_description(self, raw_job: Dict[str, Any]) -> str:
        """Extract job description."""
        pass

    @abstractmethod
    def _extract_url(self, raw_job: Dict[str, Any]) -> str:
        """Extract job URL."""
        pass

    def _extract_job_type(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract job type (full-time, part-time, etc.)."""
        return None

    def _extract_remote_type(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract remote type (remote, hybrid, onsite)."""
        return None

    def _extract_salary_min(self, raw_job: Dict[str, Any]) -> Optional[float]:
        """Extract minimum salary."""
        return None

    def _extract_salary_max(self, raw_job: Dict[str, Any]) -> Optional[float]:
        """Extract maximum salary."""
        return None

    def _extract_posted_date(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract job posted date."""
        return None

    def handle_error(self, error: Exception, context: str = ""):
        """Handle scraper errors."""
        logger.error(f"Error in {self.source_name} scraper {context}: {str(error)}")
        return []
