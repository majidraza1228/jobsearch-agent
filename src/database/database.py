"""Database connection and session management."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
from dotenv import load_dotenv

from .models import Base

load_dotenv()


class Database:
    """Database management class."""

    def __init__(self, database_url=None):
        """Initialize database connection."""
        self.database_url = database_url or os.getenv(
            "DATABASE_URL", "sqlite:///jobs.db"
        )
        self.engine = create_engine(
            self.database_url,
            echo=False,
            pool_pre_ping=True,
        )
        self.SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )

    def create_tables(self):
        """Create all tables."""
        Base.metadata.create_all(bind=self.engine)
        print("Database tables created successfully.")

    def drop_tables(self):
        """Drop all tables."""
        Base.metadata.drop_all(bind=self.engine)
        print("Database tables dropped successfully.")

    @contextmanager
    def get_session(self):
        """Get database session with context manager."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def close(self):
        """Close database connection."""
        self.SessionLocal.remove()
        self.engine.dispose()


# Global database instance
db = Database()
