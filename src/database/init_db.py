"""Initialize the database."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.database.database import db


def init_database():
    """Initialize database tables."""
    print("Initializing database...")
    db.create_tables()
    print("Database initialization complete!")


if __name__ == "__main__":
    init_database()
