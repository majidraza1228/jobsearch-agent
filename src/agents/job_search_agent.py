"""Main job search orchestration agent."""

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..scrapers import (
    IndeedScraper,
    LinkedinScraper,
    GlassdoorScraper,
    MonsterScraper,
    SerpApiScraper,
    AdzunaScraper,
)
from ..database import db, Job, SearchHistory
from .job_analyzer import JobAnalyzer

logger = logging.getLogger(__name__)


class JobSearchAgent:
    """Main orchestration agent for job search."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize job search agent.

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}

        # Initialize scrapers (including FREE alternatives)
        self.scrapers = {
            # FREE scrapers
            "serpapi": SerpApiScraper(),
            "adzuna": AdzunaScraper(),
            # PAID scrapers (RapidAPI)
            "indeed": IndeedScraper(),
            "linkedin": LinkedinScraper(),
            "glassdoor": GlassdoorScraper(),
            "monster": MonsterScraper(),
        }

        # Initialize AI analyzer with config
        ai_config = self.config.get("ai", {})
        model = ai_config.get("model", "gpt-3.5-turbo")
        provider = ai_config.get("provider")  # Optional, auto-detected
        self.analyzer = JobAnalyzer(model=model, provider=provider)

    def search_all_platforms(
        self, keywords: str, location: str = "", **kwargs
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search all enabled platforms for jobs.

        Args:
            keywords: Job search keywords
            location: Job location
            **kwargs: Additional search parameters

        Returns:
            Dictionary mapping platform name to list of jobs
        """
        results = {}

        # Get enabled scrapers from config
        enabled_scrapers = self.config.get("scrapers", {})

        for name, scraper in self.scrapers.items():
            scraper_config = enabled_scrapers.get(name, {})

            if scraper_config.get("enabled", True):
                logger.info(f"Searching {name} for '{keywords}' in '{location}'")

                try:
                    jobs = scraper.search_jobs(keywords, location, **kwargs)
                    results[name] = jobs
                    logger.info(f"Found {len(jobs)} jobs on {name}")
                except Exception as e:
                    logger.error(f"Error searching {name}: {str(e)}")
                    results[name] = []

        return results

    def save_jobs_to_db(self, jobs: List[Dict[str, Any]]) -> int:
        """
        Save jobs to database, avoiding duplicates.

        Args:
            jobs: List of job dictionaries

        Returns:
            Number of new jobs saved
        """
        saved_count = 0

        with db.get_session() as session:
            for job_data in jobs:
                external_id = job_data.get("external_id")

                if not external_id:
                    logger.warning("Job missing external_id, skipping")
                    continue

                # Check if job already exists
                existing_job = (
                    session.query(Job)
                    .filter(Job.external_id == external_id)
                    .first()
                )

                if existing_job:
                    logger.debug(f"Job {external_id} already exists, skipping")
                    continue

                # Create new job
                job = Job(
                    external_id=external_id,
                    source=job_data.get("source"),
                    title=job_data.get("title"),
                    company=job_data.get("company"),
                    location=job_data.get("location"),
                    description=job_data.get("description"),
                    url=job_data.get("url"),
                    job_type=job_data.get("job_type"),
                    remote_type=job_data.get("remote_type"),
                    salary_min=job_data.get("salary_min"),
                    salary_max=job_data.get("salary_max"),
                    required_skills=job_data.get("required_skills"),
                    required_experience_years=job_data.get("required_experience_years"),
                    education_level=job_data.get("education_level"),
                    ai_summary=job_data.get("ai_summary"),
                    ai_extracted_skills=job_data.get("ai_extracted_skills"),
                    match_score=job_data.get("match_score"),
                    posted_date=job_data.get("posted_date"),
                    raw_data=job_data.get("raw_data"),
                )

                session.add(job)
                saved_count += 1

            session.commit()

        logger.info(f"Saved {saved_count} new jobs to database")
        return saved_count

    def save_search_history(
        self, keywords: str, location: str, source: str, results_count: int, **kwargs
    ):
        """Save search history to database."""
        with db.get_session() as session:
            history = SearchHistory(
                keywords=keywords,
                location=location,
                source=source,
                results_count=results_count,
                parameters=kwargs,
            )
            session.add(history)
            session.commit()

    def execute_search(
        self,
        keywords: str,
        location: str = "",
        analyze: bool = True,
        save_to_db: bool = True,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Execute complete job search workflow.

        Args:
            keywords: Job search keywords
            location: Job location
            analyze: Whether to analyze jobs with AI
            save_to_db: Whether to save results to database
            **kwargs: Additional search parameters

        Returns:
            Dictionary with search results and statistics
        """
        logger.info(f"Starting job search for '{keywords}' in '{location}'")

        # Search all platforms
        platform_results = self.search_all_platforms(keywords, location, **kwargs)

        # Combine all jobs
        all_jobs = []
        for platform, jobs in platform_results.items():
            all_jobs.extend(jobs)

        logger.info(f"Total jobs found across all platforms: {len(all_jobs)}")

        # Analyze jobs with AI
        if analyze and all_jobs:
            logger.info("Analyzing jobs with AI...")
            all_jobs = self.analyzer.batch_analyze_jobs(all_jobs)

        # Save to database
        new_jobs_count = 0
        if save_to_db and all_jobs:
            new_jobs_count = self.save_jobs_to_db(all_jobs)

            # Save search history for each platform
            for platform, jobs in platform_results.items():
                self.save_search_history(
                    keywords=keywords,
                    location=location,
                    source=platform,
                    results_count=len(jobs),
                    **kwargs,
                )

        # Prepare response
        response = {
            "keywords": keywords,
            "location": location,
            "total_jobs": len(all_jobs),
            "new_jobs_saved": new_jobs_count,
            "platform_breakdown": {
                platform: len(jobs) for platform, jobs in platform_results.items()
            },
            "jobs": all_jobs,
            "timestamp": datetime.utcnow().isoformat(),
        }

        logger.info(f"Search complete. Found {len(all_jobs)} jobs, saved {new_jobs_count} new jobs")

        return response

    def get_jobs_from_db(
        self,
        limit: int = 100,
        source: Optional[str] = None,
        keywords: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieve jobs from database.

        Args:
            limit: Maximum number of jobs to return
            source: Filter by source platform
            keywords: Filter by keywords in title or description

        Returns:
            List of job dictionaries
        """
        with db.get_session() as session:
            query = session.query(Job).filter(Job.is_active == True)

            if source:
                query = query.filter(Job.source == source)

            if keywords:
                query = query.filter(
                    (Job.title.ilike(f"%{keywords}%"))
                    | (Job.description.ilike(f"%{keywords}%"))
                )

            jobs = query.order_by(Job.scraped_date.desc()).limit(limit).all()

            return [job.to_dict() for job in jobs]
