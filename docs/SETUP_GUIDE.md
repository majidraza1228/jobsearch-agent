# Setup Guide

Complete setup instructions for the Job Search AI Agent.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [API Keys Setup](#api-keys-setup)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)

## System Requirements

- Python 3.9 or higher
- pip (Python package manager)
- 500MB free disk space
- Internet connection

## API Keys Setup

You'll need API keys from the following services:

### 1. RapidAPI (Required)

RapidAPI provides access to job search APIs for Indeed, LinkedIn, Glassdoor, and Monster.

**Steps:**
1. Go to [RapidAPI](https://rapidapi.com/)
2. Sign up for a free account
3. Subscribe to the following APIs:
   - [Indeed Jobs API](https://rapidapi.com/hub)
   - [LinkedIn Data API](https://rapidapi.com/hub)
   - [Glassdoor Jobs API](https://rapidapi.com/hub)
   - [Monster Jobs API](https://rapidapi.com/hub)
4. Copy your RapidAPI key (found in your dashboard)

**Note:** Free tier limits vary by API. Check each API's pricing page.

### 2. OpenAI API (Required for AI Analysis)

OpenAI powers the job analysis and matching features.

**Steps:**
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (you won't be able to see it again)

**Cost:** GPT-4 costs vary. Consider using GPT-3.5-turbo for lower costs.

### 3. Alternative: SerpAPI (Optional)

As an alternative to individual RapidAPI subscriptions, you can use SerpAPI for Google Jobs results.

**Steps:**
1. Go to [SerpAPI](https://serpapi.com/)
2. Sign up for an account
3. Get your API key from the dashboard

## Installation

### 1. Clone or Download the Repository

If you have git:
```bash
git clone <repository-url>
cd jobsearch-agent
```

Or download and extract the ZIP file.

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required Python packages including:
- Flask (API server)
- SQLAlchemy (Database)
- OpenAI (AI analysis)
- Requests (HTTP client)
- And more...

## Configuration

### 1. Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# API Keys
RAPIDAPI_KEY=your_rapidapi_key_here
OPENAI_API_KEY=your_openai_key_here

# Optional: SerpAPI
SERPAPI_KEY=your_serpapi_key_here

# Database (default SQLite)
DATABASE_URL=sqlite:///jobs.db

# API Server Settings
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_ENV=development

# Search Defaults
DEFAULT_LOCATION=United States
DEFAULT_JOB_COUNT=50

# Logging
LOG_LEVEL=INFO
```

### 2. Application Configuration

Edit `config/config.yaml` to customize:

```yaml
search:
  default_keywords:
    - "Software Engineer"
    - "Data Scientist"

  default_locations:
    - "Remote"
    - "United States"

  job_count: 50

scrapers:
  indeed:
    enabled: true
    max_results: 50

  linkedin:
    enabled: true
    max_results: 50

  glassdoor:
    enabled: true
    max_results: 50

  monster:
    enabled: true
    max_results: 50

ai:
  model: "gpt-4"  # or "gpt-3.5-turbo" for lower cost
  temperature: 0.7
  max_tokens: 1000
```

### 3. Initialize Database

Create the SQLite database and tables:

```bash
python src/database/init_db.py
```

You should see:
```
Initializing database...
Database tables created successfully.
Database initialization complete!
```

## Running the Application

### Option 1: Command Line Interface (CLI)

Search for jobs directly from the command line:

```bash
# Basic search
python -m src.main --search "Python Developer" --location "Remote"

# Search without AI analysis (faster)
python -m src.main --search "Data Scientist" --no-analyze

# Search and save to JSON file
python -m src.main --search "DevOps Engineer" --output results.json

# List jobs from database
python -m src.main --list --limit 20

# Filter by source
python -m src.main --list --source linkedin --limit 10
```

### Option 2: API Server (for n8n Integration)

Start the Flask API server:

```bash
python src/api/server.py
```

You should see:
```
Starting Flask server on 0.0.0.0:5000
 * Running on http://0.0.0.0:5000
```

The API will be available at `http://localhost:5000`

### Option 3: Using the Server Flag

Alternatively, use the main script with the server flag:

```bash
python -m src.main --server
```

## Verification

### Test the CLI

```bash
python -m src.main --search "Software Engineer" --location "Remote" --limit 5
```

### Test the API Server

1. Start the server:
```bash
python src/api/server.py
```

2. In another terminal, test the health endpoint:
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{"status": "healthy", "service": "job-search-agent"}
```

3. Test job search:
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Python Developer",
    "location": "Remote",
    "analyze": true
  }'
```

### Test the Database

```bash
# List jobs from database
python -m src.main --list --limit 5
```

## Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. API Key Errors

**Error:** `401 Unauthorized` or `API key invalid`

**Solution:**
- Verify API keys in `.env` file
- Check that keys are not wrapped in quotes
- Ensure you've subscribed to the APIs on RapidAPI
- Check API key hasn't expired

#### 3. Database Errors

**Error:** `sqlite3.OperationalError: no such table: jobs`

**Solution:**
```bash
python src/database/init_db.py
```

#### 4. Rate Limit Errors

**Error:** `429 Too Many Requests`

**Solution:**
- Check your RapidAPI subscription limits
- Reduce the number of concurrent searches
- Wait before retrying
- Consider upgrading your API plan

#### 5. Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use a different port
FLASK_PORT=5001 python src/api/server.py
```

#### 6. OpenAI API Errors

**Error:** `openai.error.RateLimitError`

**Solution:**
- Check your OpenAI API usage and billing
- Reduce batch size for AI analysis
- Switch to `gpt-3.5-turbo` for lower costs

#### 7. Import Errors with Relative Imports

**Error:** `ImportError: attempted relative import with no known parent package`

**Solution:**
Use the module syntax:
```bash
# Instead of: python src/main.py
# Use:
python -m src.main
```

### Getting Help

If you encounter other issues:

1. Check the logs in `logs/jobsearch.log`
2. Enable debug mode:
   ```bash
   LOG_LEVEL=DEBUG python src/api/server.py
   ```
3. Review the API documentation in `docs/API_DOCUMENTATION.md`
4. Check n8n integration guide in `docs/N8N_INTEGRATION.md`

## Next Steps

After successful setup:

1. **Configure n8n Integration**: Follow [N8N_INTEGRATION.md](N8N_INTEGRATION.md)
2. **Customize Search Parameters**: Edit `config/config.yaml`
3. **Set Up Scheduled Searches**: Use n8n workflows or cron jobs
4. **Deploy to Production**: See deployment section in README.md

## Production Deployment

For production use:

1. **Use Production WSGI Server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.api.server:app
   ```

2. **Set Up Reverse Proxy:**
   Configure Nginx or Apache

3. **Enable HTTPS:**
   Use Let's Encrypt or other SSL certificates

4. **Set Environment to Production:**
   ```env
   FLASK_ENV=production
   ```

5. **Configure Logging:**
   Set up log rotation and monitoring

6. **Database Backup:**
   Schedule regular backups of `jobs.db`

7. **Monitor API Usage:**
   Track RapidAPI and OpenAI usage to avoid overages
