"""LinkedIn job scraper using RapidAPI."""

import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base_scraper import BaseScraper


class LinkedinScraper(BaseScraper):
    """Scraper for LinkedIn jobs via RapidAPI."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize LinkedIn scraper."""
        super().__init__(api_key)
        self.api_key = api_key or os.getenv("RAPIDAPI_KEY")
        self.api_host = "linkedin-data-api.p.rapidapi.com"
        self.api_endpoint = "https://linkedin-data-api.p.rapidapi.com/search-jobs"

    def search_jobs(
        self, keywords: str, location: str = "", **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search LinkedIn for jobs.

        Args:
            keywords: Job search keywords
            location: Job location
            **kwargs: Additional parameters

        Returns:
            List of normalized job dictionaries
        """
        try:
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": self.api_host,
            }

            params = {
                "keywords": keywords,
                "locationId": self._get_location_id(location),
                "datePosted": kwargs.get("date_posted", "anyTime"),
                "sort": kwargs.get("sort", "mostRelevant"),
            }

            # Add optional filters
            if "job_type" in kwargs:
                params["jobType"] = kwargs["job_type"]
            if "experience_level" in kwargs:
                params["experienceLevel"] = kwargs["experience_level"]

            response = requests.get(
                self.api_endpoint, headers=headers, params=params, timeout=30
            )
            response.raise_for_status()

            data = response.json()
            raw_jobs = data.get("data", [])

            # Normalize jobs
            normalized_jobs = []
            for raw_job in raw_jobs:
                try:
                    normalized_job = self.normalize_job(raw_job)
                    normalized_jobs.append(normalized_job)
                except Exception as e:
                    self.handle_error(e, f"normalizing job {raw_job.get('id', 'unknown')}")

            return normalized_jobs

        except requests.exceptions.RequestException as e:
            return self.handle_error(e, "API request")
        except Exception as e:
            return self.handle_error(e, "search_jobs")

    def _get_location_id(self, location: str) -> str:
        """Convert location string to LinkedIn location ID."""
        # Common location IDs - expand as needed
        location_map = {
            "united states": "103644278",
            "remote": "103644278",  # Default to US for remote
            "new york": "102571732",
            "san francisco": "102277331",
            "london": "102299470",
        }
        return location_map.get(location.lower(), "103644278")

    def _extract_external_id(self, raw_job: Dict[str, Any]) -> str:
        """Extract unique job ID."""
        return f"linkedin_{raw_job.get('id', raw_job.get('jobId', ''))}"

    def _extract_title(self, raw_job: Dict[str, Any]) -> str:
        """Extract job title."""
        return raw_job.get("title", "")

    def _extract_company(self, raw_job: Dict[str, Any]) -> str:
        """Extract company name."""
        company = raw_job.get("company", {})
        if isinstance(company, dict):
            return company.get("name", "")
        return str(company)

    def _extract_location(self, raw_job: Dict[str, Any]) -> str:
        """Extract job location."""
        return raw_job.get("location", "")

    def _extract_description(self, raw_job: Dict[str, Any]) -> str:
        """Extract job description."""
        return raw_job.get("description", "")

    def _extract_url(self, raw_job: Dict[str, Any]) -> str:
        """Extract job URL."""
        job_id = raw_job.get("id", raw_job.get("jobId", ""))
        return raw_job.get("url", f"https://www.linkedin.com/jobs/view/{job_id}")

    def _extract_job_type(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract job type."""
        return raw_job.get("jobType", raw_job.get("employmentType"))

    def _extract_remote_type(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract remote type."""
        workplace_type = raw_job.get("workplaceType", "").lower()
        if "remote" in workplace_type:
            return "remote"
        elif "hybrid" in workplace_type:
            return "hybrid"
        return "onsite"

    def _extract_salary_min(self, raw_job: Dict[str, Any]) -> Optional[float]:
        """Extract minimum salary."""
        salary = raw_job.get("salary", {})
        if isinstance(salary, dict):
            return salary.get("min")
        return None

    def _extract_salary_max(self, raw_job: Dict[str, Any]) -> Optional[float]:
        """Extract maximum salary."""
        salary = raw_job.get("salary", {})
        if isinstance(salary, dict):
            return salary.get("max")
        return None

    def _extract_posted_date(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract job posted date."""
        posted_at = raw_job.get("postedAt", raw_job.get("listedAt"))
        if posted_at:
            try:
                if isinstance(posted_at, int):
                    return datetime.fromtimestamp(posted_at / 1000).isoformat()
                return posted_at
            except:
                pass
        return None
