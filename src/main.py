"""Main entry point for job search agent CLI."""

import argparse
import json
from dotenv import load_dotenv

from .agents import JobSearchAgent
from .database import db
from .utils import load_config, setup_logger

load_dotenv()


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Job Search AI Agent - Search jobs from multiple platforms"
    )

    parser.add_argument(
        "--search", "-s", type=str, help="Job search keywords", required=False
    )

    parser.add_argument(
        "--location", "-l", type=str, default="", help="Job location"
    )

    parser.add_argument(
        "--analyze",
        "-a",
        action="store_true",
        default=True,
        help="Analyze jobs with AI (default: True)",
    )

    parser.add_argument(
        "--no-analyze",
        action="store_true",
        help="Skip AI analysis",
    )

    parser.add_argument(
        "--save",
        action="store_true",
        default=True,
        help="Save results to database (default: True)",
    )

    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Don't save to database",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List jobs from database",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Limit number of results (default: 50)",
    )

    parser.add_argument(
        "--source",
        type=str,
        choices=["indeed", "linkedin", "glassdoor", "monster"],
        help="Filter by source platform",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output results to JSON file",
    )

    parser.add_argument(
        "--init-db",
        action="store_true",
        help="Initialize database",
    )

    parser.add_argument(
        "--server",
        action="store_true",
        help="Run Flask API server",
    )

    args = parser.parse_args()

    # Setup logger
    logger = setup_logger(log_file="logs/jobsearch.log")

    # Initialize database if requested
    if args.init_db:
        logger.info("Initializing database...")
        db.create_tables()
        logger.info("Database initialized successfully!")
        return

    # Run server if requested
    if args.server:
        from .api import run_server

        run_server()
        return

    # Load configuration
    config = load_config()

    # Initialize agent
    agent = JobSearchAgent(config=config)

    # List jobs from database
    if args.list:
        logger.info("Retrieving jobs from database...")
        jobs = agent.get_jobs_from_db(limit=args.limit, source=args.source)

        print(f"\n{'='*80}")
        print(f"Found {len(jobs)} jobs in database")
        print(f"{'='*80}\n")

        for i, job in enumerate(jobs, 1):
            print(f"{i}. {job['title']} at {job['company']}")
            print(f"   Source: {job['source']} | Location: {job['location']}")
            print(f"   URL: {job['url']}")
            print(f"   Posted: {job['posted_date']}")
            print()

        if args.output:
            with open(args.output, "w") as f:
                json.dump(jobs, f, indent=2)
            logger.info(f"Results saved to {args.output}")

        return

    # Search for jobs
    if args.search:
        analyze = args.analyze and not args.no_analyze
        save = args.save and not args.no_save

        logger.info(f"Searching for jobs: {args.search}")

        results = agent.execute_search(
            keywords=args.search,
            location=args.location,
            analyze=analyze,
            save_to_db=save,
        )

        # Print results
        print(f"\n{'='*80}")
        print(f"Search Results: {args.search}")
        if args.location:
            print(f"Location: {args.location}")
        print(f"{'='*80}\n")

        print(f"Total jobs found: {results['total_jobs']}")
        print(f"New jobs saved: {results['new_jobs_saved']}")
        print(f"\nPlatform breakdown:")
        for platform, count in results["platform_breakdown"].items():
            print(f"  - {platform}: {count}")

        print(f"\n{'='*80}")
        print("Job Listings:")
        print(f"{'='*80}\n")

        for i, job in enumerate(results["jobs"][:args.limit], 1):
            print(f"{i}. {job['title']} at {job['company']}")
            print(f"   Source: {job['source']} | Location: {job['location']}")
            print(f"   URL: {job['url']}")

            if analyze and job.get("ai_summary"):
                print(f"   AI Summary: {job['ai_summary'][:150]}...")

            print()

        # Save to file if requested
        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
            logger.info(f"Results saved to {args.output}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
