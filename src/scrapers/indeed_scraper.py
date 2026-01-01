"""Indeed job scraper using RapidAPI."""

import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base_scraper import BaseScraper


class IndeedScraper(BaseScraper):
    """Scraper for Indeed jobs via RapidAPI."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Indeed scraper."""
        super().__init__(api_key)
        self.api_key = api_key or os.getenv("RAPIDAPI_KEY")
        self.api_host = "indeed12.p.rapidapi.com"
        self.api_endpoint = "https://indeed12.p.rapidapi.com/jobs/search"

    def search_jobs(
        self, keywords: str, location: str = "", **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search Indeed for jobs.

        Args:
            keywords: Job search keywords
            location: Job location
            **kwargs: Additional parameters (page, job_type, remote, etc.)

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
                "page_id": kwargs.get("page", "1"),
                "locality": kwargs.get("locality", "us"),
            }

            # Add optional filters
            if "date_posted" in kwargs:
                params["date_posted"] = kwargs["date_posted"]
            if "job_type" in kwargs:
                params["job_type"] = kwargs["job_type"]
            if "remote" in kwargs:
                params["remote"] = kwargs["remote"]

            response = requests.get(
                self.api_endpoint, headers=headers, params=params, timeout=30
            )
            response.raise_for_status()

            data = response.json()
            raw_jobs = data.get("hits", [])

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

    def _extract_external_id(self, raw_job: Dict[str, Any]) -> str:
        """Extract unique job ID."""
        return f"indeed_{raw_job.get('id', raw_job.get('job_id', ''))}"

    def _extract_title(self, raw_job: Dict[str, Any]) -> str:
        """Extract job title."""
        return raw_job.get("title", "")

    def _extract_company(self, raw_job: Dict[str, Any]) -> str:
        """Extract company name."""
        return raw_job.get("company_name", raw_job.get("company", ""))

    def _extract_location(self, raw_job: Dict[str, Any]) -> str:
        """Extract job location."""
        location = raw_job.get("location", "")
        if isinstance(location, dict):
            city = location.get("city", "")
            state = location.get("state", "")
            return f"{city}, {state}".strip(", ")
        return location

    def _extract_description(self, raw_job: Dict[str, Any]) -> str:
        """Extract job description."""
        return raw_job.get("description", raw_job.get("snippet", ""))

    def _extract_url(self, raw_job: Dict[str, Any]) -> str:
        """Extract job URL."""
        job_id = raw_job.get("id", raw_job.get("job_id", ""))
        return raw_job.get("url", f"https://www.indeed.com/viewjob?jk={job_id}")

    def _extract_job_type(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract job type."""
        return raw_job.get("job_type", raw_job.get("employment_type"))

    def _extract_remote_type(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract remote type."""
        if raw_job.get("remote"):
            return "remote"
        return raw_job.get("remote_type", "onsite")

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
        date_str = raw_job.get("pub_date_ts_milli", raw_job.get("date_posted"))
        if date_str:
            try:
                if isinstance(date_str, int):
                    return datetime.fromtimestamp(date_str / 1000).isoformat()
                return date_str
            except:
                pass
        return None
