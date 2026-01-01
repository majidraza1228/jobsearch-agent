"""Monster job scraper using RapidAPI."""

import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base_scraper import BaseScraper


class MonsterScraper(BaseScraper):
    """Scraper for Monster jobs via RapidAPI."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Monster scraper."""
        super().__init__(api_key)
        self.api_key = api_key or os.getenv("RAPIDAPI_KEY")
        self.api_host = "monster-job-search.p.rapidapi.com"
        self.api_endpoint = "https://monster-job-search.p.rapidapi.com/search"

    def search_jobs(
        self, keywords: str, location: str = "", **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search Monster for jobs.

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
                "q": keywords,
                "where": location or "United States",
                "page": kwargs.get("page", "1"),
            }

            # Add optional filters
            if "date_posted" in kwargs:
                params["tm"] = kwargs["date_posted"]

            response = requests.get(
                self.api_endpoint, headers=headers, params=params, timeout=30
            )
            response.raise_for_status()

            data = response.json()
            raw_jobs = data.get("results", [])

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
        return f"monster_{raw_job.get('id', raw_job.get('jobId', ''))}"

    def _extract_title(self, raw_job: Dict[str, Any]) -> str:
        """Extract job title."""
        return raw_job.get("title", raw_job.get("jobTitle", ""))

    def _extract_company(self, raw_job: Dict[str, Any]) -> str:
        """Extract company name."""
        company = raw_job.get("company", {})
        if isinstance(company, dict):
            return company.get("name", "")
        return str(company)

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
        return raw_job.get("description", raw_job.get("summary", ""))

    def _extract_url(self, raw_job: Dict[str, Any]) -> str:
        """Extract job URL."""
        return raw_job.get("url", raw_job.get("applyUrl", ""))

    def _extract_job_type(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract job type."""
        return raw_job.get("jobType", raw_job.get("employmentType"))

    def _extract_remote_type(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract remote type."""
        if raw_job.get("isRemote"):
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
        date_str = raw_job.get("postedDate", raw_job.get("datePosted"))
        if date_str:
            try:
                return datetime.fromisoformat(date_str.replace("Z", "+00:00")).isoformat()
            except:
                pass
        return None
