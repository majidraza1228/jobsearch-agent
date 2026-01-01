"""Database models for job search agent."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Job(Base):
    """Job posting model."""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(255), unique=True, nullable=False, index=True)
    source = Column(String(50), nullable=False, index=True)  # indeed, linkedin, etc.

    # Basic job info
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255))
    description = Column(Text)
    url = Column(String(512))

    # Employment details
    job_type = Column(String(50))  # full-time, part-time, contract
    remote_type = Column(String(50))  # remote, hybrid, onsite
    salary_min = Column(Float)
    salary_max = Column(Float)
    salary_currency = Column(String(10), default="USD")

    # Requirements
    required_skills = Column(JSON)  # List of skills
    required_experience_years = Column(Integer)
    education_level = Column(String(100))

    # AI Analysis
    ai_summary = Column(Text)
    ai_extracted_skills = Column(JSON)
    match_score = Column(Float)  # If matching against user profile

    # Metadata
    posted_date = Column(DateTime)
    scraped_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Raw data
    raw_data = Column(JSON)  # Store original API response

    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', company='{self.company}')>"

    def to_dict(self):
        """Convert job to dictionary."""
        return {
            "id": self.id,
            "external_id": self.external_id,
            "source": self.source,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "url": self.url,
            "job_type": self.job_type,
            "remote_type": self.remote_type,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "salary_currency": self.salary_currency,
            "required_skills": self.required_skills,
            "required_experience_years": self.required_experience_years,
            "education_level": self.education_level,
            "ai_summary": self.ai_summary,
            "ai_extracted_skills": self.ai_extracted_skills,
            "match_score": self.match_score,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "scraped_date": self.scraped_date.isoformat() if self.scraped_date else None,
            "updated_date": self.updated_date.isoformat() if self.updated_date else None,
            "is_active": self.is_active,
        }


class SearchHistory(Base):
    """Track search queries."""

    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    keywords = Column(String(255), nullable=False)
    location = Column(String(255))
    source = Column(String(50))
    results_count = Column(Integer)
    search_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    parameters = Column(JSON)  # Store all search parameters

    def __repr__(self):
        return f"<SearchHistory(keywords='{self.keywords}', location='{self.location}')>"


class UserProfile(Base):
    """User profile for job matching."""

    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255), unique=True)

    # Skills and experience
    skills = Column(JSON)  # List of skills
    experience_years = Column(Integer)
    education_level = Column(String(100))

    # Preferences
    preferred_job_types = Column(JSON)  # List of job types
    preferred_locations = Column(JSON)  # List of locations
    preferred_remote_type = Column(String(50))
    salary_expectation_min = Column(Float)
    salary_expectation_max = Column(Float)

    # Resume
    resume_text = Column(Text)

    # Metadata
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<UserProfile(name='{self.name}', email='{self.email}')>"
