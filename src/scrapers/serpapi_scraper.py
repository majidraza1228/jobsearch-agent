"""SerpAPI job scraper - Free alternative to RapidAPI."""

import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base_scraper import BaseScraper


class SerpApiScraper(BaseScraper):
    """
    Scraper using SerpAPI for Google Jobs.

    Free tier: 100 searches/month
    Sign up at: https://serpapi.com/

    This aggregates jobs from all platforms:
    - Indeed
    - LinkedIn
    - Glassdoor
    - ZipRecruiter
    - Monster
    - And more!
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize SerpAPI scraper."""
        super().__init__(api_key)
        self.api_key = api_key or os.getenv("SERPAPI_KEY")
        self.api_endpoint = "https://serpapi.com/search"

    def search_jobs(
        self, keywords: str, location: str = "", **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search Google Jobs via SerpAPI.

        Args:
            keywords: Job search keywords
            location: Job location
            **kwargs: Additional parameters

        Returns:
            List of normalized job dictionaries
        """
        try:
            params = {
                "api_key": self.api_key,
                "engine": "google_jobs",
                "q": keywords,
                "location": location or "United States",
                "hl": "en",
                "gl": "us",
            }

            # Add optional filters
            if "chips" in kwargs:
                params["chips"] = kwargs["chips"]  # date_posted, employment_type, etc.

            response = requests.get(
                self.api_endpoint, params=params, timeout=30
            )
            response.raise_for_status()

            data = response.json()
            raw_jobs = data.get("jobs_results", [])

            # Normalize jobs
            normalized_jobs = []
            for raw_job in raw_jobs:
                try:
                    normalized_job = self.normalize_job(raw_job)
                    normalized_jobs.append(normalized_job)
                except Exception as e:
                    self.handle_error(e, f"normalizing job {raw_job.get('job_id', 'unknown')}")

            return normalized_jobs

        except requests.exceptions.RequestException as e:
            return self.handle_error(e, "API request")
        except Exception as e:
            return self.handle_error(e, "search_jobs")

    def _extract_external_id(self, raw_job: Dict[str, Any]) -> str:
        """Extract unique job ID."""
        return f"serpapi_{raw_job.get('job_id', '')}"

    def _extract_title(self, raw_job: Dict[str, Any]) -> str:
        """Extract job title."""
        return raw_job.get("title", "")

    def _extract_company(self, raw_job: Dict[str, Any]) -> str:
        """Extract company name."""
        return raw_job.get("company_name", "")

    def _extract_location(self, raw_job: Dict[str, Any]) -> str:
        """Extract job location."""
        return raw_job.get("location", "")

    def _extract_description(self, raw_job: Dict[str, Any]) -> str:
        """Extract job description."""
        description = raw_job.get("description", "")
        # Also get highlights if available
        highlights = raw_job.get("job_highlights", [])
        if highlights:
            description += "\n\nHighlights:\n"
            for section in highlights:
                title = section.get("title", "")
                items = section.get("items", [])
                if items:
                    description += f"\n{title}:\n"
                    description += "\n".join(f"- {item}" for item in items)
        return description

    def _extract_url(self, raw_job: Dict[str, Any]) -> str:
        """Extract job URL."""
        # Try multiple URL fields
        for field in ["share_url", "apply_options", "related_links"]:
            url = raw_job.get(field)
            if url:
                if isinstance(url, list) and len(url) > 0:
                    return url[0].get("link", "")
                elif isinstance(url, str):
                    return url
        return ""

    def _extract_job_type(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract job type."""
        detected_extensions = raw_job.get("detected_extensions", {})
        return detected_extensions.get("schedule_type")

    def _extract_remote_type(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract remote type."""
        detected_extensions = raw_job.get("detected_extensions", {})
        work_from_home = detected_extensions.get("work_from_home", False)
        if work_from_home:
            return "remote"
        return "onsite"

    def _extract_posted_date(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract job posted date."""
        detected_extensions = raw_job.get("detected_extensions", {})
        posted_at = detected_extensions.get("posted_at")
        if posted_at:
            return posted_at
        return None
