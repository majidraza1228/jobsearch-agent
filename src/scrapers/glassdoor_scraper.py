"""Glassdoor job scraper using RapidAPI."""

import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base_scraper import BaseScraper


class GlassdoorScraper(BaseScraper):
    """Scraper for Glassdoor jobs via RapidAPI."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Glassdoor scraper."""
        super().__init__(api_key)
        self.api_key = api_key or os.getenv("RAPIDAPI_KEY")
        self.api_host = "glassdoor-job-search.p.rapidapi.com"
        self.api_endpoint = "https://glassdoor-job-search.p.rapidapi.com/search"

    def search_jobs(
        self, keywords: str, location: str = "", **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search Glassdoor for jobs.

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
                "query": keywords,
                "location": location or "United States",
                "page": kwargs.get("page", "1"),
            }

            # Add optional filters
            if "date_posted" in kwargs:
                params["fromAge"] = kwargs["date_posted"]
            if "job_type" in kwargs:
                params["employmentType"] = kwargs["job_type"]

            response = requests.get(
                self.api_endpoint, headers=headers, params=params, timeout=30
            )
            response.raise_for_status()

            data = response.json()
            raw_jobs = data.get("jobs", [])

            # Normalize jobs
            normalized_jobs = []
            for raw_job in raw_jobs:
                try:
                    normalized_job = self.normalize_job(raw_job)
                    normalized_jobs.append(normalized_job)
                except Exception as e:
                    self.handle_error(e, f"normalizing job {raw_job.get('jobId', 'unknown')}")

            return normalized_jobs

        except requests.exceptions.RequestException as e:
            return self.handle_error(e, "API request")
        except Exception as e:
            return self.handle_error(e, "search_jobs")

    def _extract_external_id(self, raw_job: Dict[str, Any]) -> str:
        """Extract unique job ID."""
        return f"glassdoor_{raw_job.get('jobId', '')}"

    def _extract_title(self, raw_job: Dict[str, Any]) -> str:
        """Extract job title."""
        return raw_job.get("jobTitle", raw_job.get("title", ""))

    def _extract_company(self, raw_job: Dict[str, Any]) -> str:
        """Extract company name."""
        employer = raw_job.get("employer", {})
        if isinstance(employer, dict):
            return employer.get("name", "")
        return str(employer)

    def _extract_location(self, raw_job: Dict[str, Any]) -> str:
        """Extract job location."""
        location = raw_job.get("location", {})
        if isinstance(location, dict):
            return location.get("name", "")
        return str(location)

    def _extract_description(self, raw_job: Dict[str, Any]) -> str:
        """Extract job description."""
        return raw_job.get("description", raw_job.get("jobDescription", ""))

    def _extract_url(self, raw_job: Dict[str, Any]) -> str:
        """Extract job URL."""
        return raw_job.get("jobUrl", raw_job.get("url", ""))

    def _extract_job_type(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract job type."""
        return raw_job.get("employmentType")

    def _extract_remote_type(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract remote type."""
        location = raw_job.get("location", {})
        if isinstance(location, dict):
            if location.get("isRemote"):
                return "remote"
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
        date_str = raw_job.get("postedDate", raw_job.get("listingDate"))
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00")).isoformat()
            except:
                pass
        return None
