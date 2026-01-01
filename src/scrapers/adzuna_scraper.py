"""Adzuna API job scraper - Free alternative."""

import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime

from .base_scraper import BaseScraper


class AdzunaScraper(BaseScraper):
    """
    Scraper using Adzuna API.

    Free tier: 250 calls/month
    Sign up at: https://developer.adzuna.com/

    Coverage: US, UK, AU, CA, and many more countries
    """

    def __init__(self, app_id: Optional[str] = None, app_key: Optional[str] = None):
        """Initialize Adzuna scraper."""
        super().__init__(app_key)
        self.app_id = app_id or os.getenv("ADZUNA_APP_ID")
        self.app_key = app_key or os.getenv("ADZUNA_APP_KEY")
        self.api_endpoint = "https://api.adzuna.com/v1/api/jobs/us/search/1"

    def search_jobs(
        self, keywords: str, location: str = "", **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search Adzuna for jobs.

        Args:
            keywords: Job search keywords
            location: Job location
            **kwargs: Additional parameters

        Returns:
            List of normalized job dictionaries
        """
        try:
            params = {
                "app_id": self.app_id,
                "app_key": self.app_key,
                "what": keywords,
                "where": location,
                "results_per_page": kwargs.get("results_per_page", 50),
                "content-type": "application/json",
            }

            # Add optional filters
            if "max_days_old" in kwargs:
                params["max_days_old"] = kwargs["max_days_old"]
            if "salary_min" in kwargs:
                params["salary_min"] = kwargs["salary_min"]

            response = requests.get(
                self.api_endpoint, params=params, timeout=30
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
        return f"adzuna_{raw_job.get('id', '')}"

    def _extract_title(self, raw_job: Dict[str, Any]) -> str:
        """Extract job title."""
        return raw_job.get("title", "")

    def _extract_company(self, raw_job: Dict[str, Any]) -> str:
        """Extract company name."""
        company = raw_job.get("company", {})
        if isinstance(company, dict):
            return company.get("display_name", "")
        return str(company)

    def _extract_location(self, raw_job: Dict[str, Any]) -> str:
        """Extract job location."""
        location = raw_job.get("location", {})
        if isinstance(location, dict):
            areas = location.get("display_name", "")
            return areas
        return str(location)

    def _extract_description(self, raw_job: Dict[str, Any]) -> str:
        """Extract job description."""
        return raw_job.get("description", "")

    def _extract_url(self, raw_job: Dict[str, Any]) -> str:
        """Extract job URL."""
        return raw_job.get("redirect_url", "")

    def _extract_job_type(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract job type."""
        contract_type = raw_job.get("contract_type")
        if contract_type:
            return contract_type.lower().replace("_", "-")
        return None

    def _extract_salary_min(self, raw_job: Dict[str, Any]) -> Optional[float]:
        """Extract minimum salary."""
        return raw_job.get("salary_min")

    def _extract_salary_max(self, raw_job: Dict[str, Any]) -> Optional[float]:
        """Extract maximum salary."""
        return raw_job.get("salary_max")

    def _extract_posted_date(self, raw_job: Dict[str, Any]) -> Optional[str]:
        """Extract job posted date."""
        created = raw_job.get("created")
        if created:
            return created
        return None
