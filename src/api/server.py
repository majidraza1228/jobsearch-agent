"""Flask API server for n8n integration."""

import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import yaml

from ..agents import JobSearchAgent
from ..database import db

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load configuration
config_path = os.path.join(
    os.path.dirname(__file__), "../../config/config.yaml"
)
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# Initialize job search agent
agent = JobSearchAgent(config=config)


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "job-search-agent"}), 200


@app.route("/api/search", methods=["POST"])
def search_jobs():
    """
    Search for jobs across all platforms.

    Request body:
    {
        "keywords": "Python Developer",
        "location": "Remote",
        "analyze": true,
        "save_to_db": true
    }

    Returns:
    {
        "keywords": "Python Developer",
        "location": "Remote",
        "total_jobs": 150,
        "new_jobs_saved": 45,
        "platform_breakdown": {...},
        "jobs": [...]
    }
    """
    try:
        data = request.get_json()

        if not data or "keywords" not in data:
            return jsonify({"error": "Missing required field: keywords"}), 400

        keywords = data.get("keywords")
        location = data.get("location", "")
        analyze = data.get("analyze", True)
        save_to_db = data.get("save_to_db", True)

        # Optional parameters
        kwargs = {}
        if "page" in data:
            kwargs["page"] = data["page"]
        if "date_posted" in data:
            kwargs["date_posted"] = data["date_posted"]
        if "job_type" in data:
            kwargs["job_type"] = data["job_type"]

        logger.info(f"Received search request: {keywords} in {location}")

        # Execute search
        results = agent.execute_search(
            keywords=keywords,
            location=location,
            analyze=analyze,
            save_to_db=save_to_db,
            **kwargs,
        )

        return jsonify(results), 200

    except Exception as e:
        logger.error(f"Error in search endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    """
    Retrieve jobs from database.

    Query parameters:
    - limit: Maximum number of jobs (default: 100)
    - source: Filter by platform (indeed, linkedin, etc.)
    - keywords: Filter by keywords in title/description

    Returns:
    {
        "count": 100,
        "jobs": [...]
    }
    """
    try:
        limit = int(request.args.get("limit", 100))
        source = request.args.get("source")
        keywords = request.args.get("keywords")

        jobs = agent.get_jobs_from_db(limit=limit, source=source, keywords=keywords)

        return jsonify({"count": len(jobs), "jobs": jobs}), 200

    except Exception as e:
        logger.error(f"Error in get_jobs endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/jobs/<int:job_id>", methods=["GET"])
def get_job(job_id):
    """
    Get a specific job by ID.

    Returns:
    {
        "id": 123,
        "title": "...",
        ...
    }
    """
    try:
        from ..database import Job

        with db.get_session() as session:
            job = session.query(Job).filter(Job.id == job_id).first()

            if not job:
                return jsonify({"error": "Job not found"}), 404

            return jsonify(job.to_dict()), 200

    except Exception as e:
        logger.error(f"Error in get_job endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/webhook/job-search", methods=["POST"])
def n8n_webhook():
    """
    n8n webhook endpoint for job search.

    This endpoint is designed to be called from n8n workflows.

    Request body:
    {
        "keywords": "Python Developer",
        "location": "Remote",
        "options": {
            "analyze": true,
            "save_to_db": true
        }
    }

    Returns the same format as /api/search
    """
    try:
        data = request.get_json()

        if not data or "keywords" not in data:
            return jsonify({"error": "Missing required field: keywords"}), 400

        keywords = data.get("keywords")
        location = data.get("location", "")
        options = data.get("options", {})

        analyze = options.get("analyze", True)
        save_to_db = options.get("save_to_db", True)

        logger.info(f"n8n webhook triggered: {keywords} in {location}")

        # Execute search
        results = agent.execute_search(
            keywords=keywords,
            location=location,
            analyze=analyze,
            save_to_db=save_to_db,
        )

        # Format response for n8n
        n8n_response = {
            "success": True,
            "message": f"Found {results['total_jobs']} jobs, saved {results['new_jobs_saved']} new jobs",
            "data": results,
        }

        return jsonify(n8n_response), 200

    except Exception as e:
        logger.error(f"Error in n8n webhook: {str(e)}", exc_info=True)
        return (
            jsonify({"success": False, "error": str(e), "message": "Search failed"}),
            500,
        )


@app.route("/api/analyze", methods=["POST"])
def analyze_job():
    """
    Analyze a job description with AI.

    Request body:
    {
        "title": "Software Engineer",
        "description": "We are looking for..."
    }

    Returns:
    {
        "required_skills": [...],
        "summary": "...",
        ...
    }
    """
    try:
        data = request.get_json()

        if not data or "description" not in data:
            return jsonify({"error": "Missing required field: description"}), 400

        from ..agents import JobAnalyzer

        analyzer = JobAnalyzer()
        analysis = analyzer.analyze_job(data)

        return jsonify(analysis), 200

    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/api/stats", methods=["GET"])
def get_stats():
    """
    Get database statistics.

    Returns:
    {
        "total_jobs": 1234,
        "jobs_by_source": {...},
        "recent_searches": 50
    }
    """
    try:
        from ..database import Job, SearchHistory

        with db.get_session() as session:
            total_jobs = session.query(Job).filter(Job.is_active == True).count()

            # Jobs by source
            jobs_by_source = {}
            for source in ["indeed", "linkedin", "glassdoor", "monster"]:
                count = (
                    session.query(Job)
                    .filter(Job.source == source, Job.is_active == True)
                    .count()
                )
                jobs_by_source[source] = count

            # Recent searches
            recent_searches = session.query(SearchHistory).count()

            stats = {
                "total_jobs": total_jobs,
                "jobs_by_source": jobs_by_source,
                "recent_searches": recent_searches,
            }

            return jsonify(stats), 200

    except Exception as e:
        logger.error(f"Error in stats endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


def run_server():
    """Run the Flask server."""
    # Initialize database
    db.create_tables()

    # Get configuration from environment
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_ENV", "production") == "development"

    logger.info(f"Starting Flask server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_server()
