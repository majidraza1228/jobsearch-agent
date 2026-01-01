"""AI agent for analyzing job postings."""

import os
from typing import Dict, Any, List, Optional
import json
import logging

logger = logging.getLogger(__name__)


class JobAnalyzer:
    """AI-powered job analyzer using OpenAI or Anthropic."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        provider: Optional[str] = None,
    ):
        """
        Initialize job analyzer.

        Args:
            api_key: API key (OpenAI or Anthropic)
            model: Model to use (gpt-4, gpt-3.5-turbo, claude-3-5-sonnet-20241022, etc.)
            provider: "openai" or "anthropic" (auto-detected if not specified)
        """
        # Auto-detect provider if not specified
        if provider is None:
            if "claude" in model.lower():
                provider = "anthropic"
            else:
                provider = "openai"

        self.provider = provider
        self.model = model

        # Initialize the appropriate client
        if self.provider == "anthropic":
            try:
                from anthropic import Anthropic

                self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
                self.client = Anthropic(api_key=self.api_key)
                logger.info(f"Using Anthropic Claude: {model}")
            except ImportError:
                logger.error(
                    "Anthropic package not installed. Install with: pip install anthropic"
                )
                raise
        else:  # openai
            try:
                from openai import OpenAI

                self.api_key = api_key or os.getenv("OPENAI_API_KEY")
                self.client = OpenAI(api_key=self.api_key)
                logger.info(f"Using OpenAI: {model}")
            except ImportError:
                logger.error("OpenAI package not installed. Install with: pip install openai")
                raise

    def analyze_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a job posting and extract structured information.

        Args:
            job: Job dictionary with description

        Returns:
            Dictionary with analyzed information
        """
        try:
            description = job.get("description", "")
            title = job.get("title", "")

            if not description:
                logger.warning(f"No description for job: {title}")
                return {}

            prompt = f"""Analyze the following job posting and extract structured information.

Job Title: {title}
Job Description: {description}

Extract and return a JSON object with the following fields:
{{
    "required_skills": ["list", "of", "skills"],
    "preferred_skills": ["list", "of", "preferred", "skills"],
    "experience_years": <number or null>,
    "education_level": "Bachelor's/Master's/PhD/etc or null",
    "remote_friendly": true/false,
    "key_responsibilities": ["list", "of", "main", "responsibilities"],
    "technologies": ["list", "of", "specific", "technologies"],
    "soft_skills": ["list", "of", "soft", "skills"],
    "salary_indicators": "any salary information mentioned",
    "summary": "brief 2-3 sentence summary of the role"
}}

Return ONLY the JSON object, no other text."""

            # Call appropriate AI provider
            if self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    temperature=0.3,
                    system="You are a job posting analyzer. Extract structured information from job descriptions and return valid JSON.",
                    messages=[{"role": "user", "content": prompt}],
                )
                result = response.content[0].text
            else:  # openai
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a job posting analyzer. Extract structured information from job descriptions and return valid JSON.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                    max_tokens=1000,
                )
                result = response.choices[0].message.content

            # Parse JSON response
            try:
                analysis = json.loads(result)
                return analysis
            except json.JSONDecodeError:
                # Try to extract JSON from markdown code blocks
                if "```json" in result:
                    json_str = result.split("```json")[1].split("```")[0].strip()
                    analysis = json.loads(json_str)
                    return analysis
                elif "```" in result:
                    json_str = result.split("```")[1].split("```")[0].strip()
                    analysis = json.loads(json_str)
                    return analysis
                else:
                    logger.error(f"Failed to parse JSON response: {result}")
                    return {}

        except Exception as e:
            logger.error(f"Error analyzing job: {str(e)}")
            return {}

    def match_job_to_profile(
        self, job: Dict[str, Any], user_profile: Dict[str, Any]
    ) -> float:
        """
        Calculate match score between job and user profile.

        Args:
            job: Job dictionary
            user_profile: User profile dictionary

        Returns:
            Match score between 0 and 100
        """
        try:
            job_analysis = job.get("ai_extracted_skills", {})
            user_skills = user_profile.get("skills", [])

            if not job_analysis or not user_skills:
                return 0.0

            required_skills = job_analysis.get("required_skills", [])
            technologies = job_analysis.get("technologies", [])

            # Combine all job requirements
            all_job_skills = set(
                skill.lower() for skill in (required_skills + technologies)
            )
            user_skills_set = set(skill.lower() for skill in user_skills)

            if not all_job_skills:
                return 0.0

            # Calculate overlap
            matching_skills = all_job_skills.intersection(user_skills_set)
            match_ratio = len(matching_skills) / len(all_job_skills)

            # Adjust for experience
            job_experience = job_analysis.get("experience_years", 0) or 0
            user_experience = user_profile.get("experience_years", 0) or 0

            experience_match = 1.0
            if job_experience > 0:
                if user_experience >= job_experience:
                    experience_match = 1.0
                else:
                    experience_match = user_experience / job_experience

            # Calculate final score (70% skills, 30% experience)
            final_score = (match_ratio * 0.7 + experience_match * 0.3) * 100

            return round(final_score, 2)

        except Exception as e:
            logger.error(f"Error matching job to profile: {str(e)}")
            return 0.0

    def batch_analyze_jobs(
        self, jobs: List[Dict[str, Any]], max_jobs: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Analyze multiple jobs in batch.

        Args:
            jobs: List of job dictionaries
            max_jobs: Maximum number of jobs to analyze

        Returns:
            List of jobs with analysis added
        """
        analyzed_jobs = []

        for i, job in enumerate(jobs[:max_jobs]):
            logger.info(f"Analyzing job {i+1}/{min(len(jobs), max_jobs)}: {job.get('title')}")

            analysis = self.analyze_job(job)
            job["ai_extracted_skills"] = analysis.get("required_skills", [])
            job["ai_summary"] = analysis.get("summary", "")

            # Store full analysis in raw_data if it exists
            if "raw_data" not in job:
                job["raw_data"] = {}
            job["raw_data"]["ai_analysis"] = analysis

            analyzed_jobs.append(job)

        return analyzed_jobs
