# Quick Start Guide

Get started with the Job Search AI Agent in 5 minutes!

## Prerequisites

- Python 3.9+
- API Keys (RapidAPI + OpenAI)

## Step 1: Get API Keys

### RapidAPI Key
1. Sign up at [RapidAPI](https://rapidapi.com/)
2. Subscribe to job search APIs (Indeed, LinkedIn, Glassdoor, Monster)
3. Copy your API key

### OpenAI Key
1. Sign up at [OpenAI](https://platform.openai.com/)
2. Create an API key
3. Copy the key

## Step 2: Setup

### Automated Setup (Recommended)

**macOS/Linux:**
```bash
./run.sh
```

**Windows:**
```bash
run.bat
```

### Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your API keys

# 5. Initialize database
python src/database/init_db.py
```

## Step 3: Configure API Keys

Edit `.env` file:

```env
RAPIDAPI_KEY=your_rapidapi_key_here
OPENAI_API_KEY=your_openai_key_here
```

## Step 4: Run

### Option A: Search Jobs (CLI)

```bash
python -m src.main --search "Python Developer" --location "Remote"
```

### Option B: Start API Server (for n8n)

```bash
python src/api/server.py
```

Server will start at `http://localhost:5000`

### Option C: Test with cURL

```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Software Engineer",
    "location": "Remote",
    "analyze": true
  }'
```

## Step 5: n8n Integration

1. Start the API server (Step 4, Option B)
2. Open n8n
3. Import workflow from `n8n-workflows/job-search-workflow.json`
4. Trigger the workflow

## Common Commands

```bash
# Search for jobs
python -m src.main --search "Data Scientist" --location "New York"

# Search without AI (faster)
python -m src.main --search "DevOps" --no-analyze

# List saved jobs
python -m src.main --list --limit 20

# Filter by platform
python -m src.main --list --source linkedin

# Export to JSON
python -m src.main --search "Manager" --output results.json

# Start API server
python src/api/server.py

# Initialize database
python src/database/init_db.py
```

## Project Structure

```
jobsearch-agent/
├── src/
│   ├── scrapers/       # Job scrapers (Indeed, LinkedIn, etc.)
│   ├── agents/         # AI analysis and orchestration
│   ├── database/       # SQLite database models
│   ├── api/            # Flask API server
│   └── utils/          # Helper utilities
├── config/
│   └── config.yaml     # Application configuration
├── n8n-workflows/      # n8n workflow templates
├── docs/               # Documentation
│   ├── SETUP_GUIDE.md
│   ├── API_DOCUMENTATION.md
│   └── N8N_INTEGRATION.md
└── README.md
```

## API Endpoints

- `GET /health` - Health check
- `POST /api/search` - Search jobs
- `GET /api/jobs` - Get saved jobs
- `GET /api/jobs/{id}` - Get specific job
- `POST /webhook/job-search` - n8n webhook
- `POST /api/analyze` - Analyze job description
- `GET /api/stats` - Database statistics

## Configuration

Edit `config/config.yaml` to customize:

- Default search keywords and locations
- Enable/disable specific platforms
- AI model settings (GPT-4 vs GPT-3.5-turbo)
- API rate limits
- Database settings

## Troubleshooting

**Import Error:**
```bash
# Use module syntax
python -m src.main
```

**Port in use:**
```bash
FLASK_PORT=5001 python src/api/server.py
```

**Database not found:**
```bash
python src/database/init_db.py
```

**API key errors:**
- Check .env file has correct keys
- Verify API subscriptions on RapidAPI
- Check OpenAI billing

## Next Steps

1. Read [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for detailed setup
2. Review [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for API reference
3. Follow [N8N_INTEGRATION.md](docs/N8N_INTEGRATION.md) for n8n workflows
4. Customize `config/config.yaml` for your needs

## Example Workflows

### Daily Job Digest (n8n)
1. Schedule trigger (9 AM daily)
2. Search multiple keywords
3. Send email digest
4. Save to database

### Job Application Tracker
1. Search for relevant jobs
2. Filter by match score
3. Store in Airtable/Sheets
4. Track application status

### Smart Job Alerts
1. Continuous job monitoring
2. AI-powered matching
3. Slack/Email notifications
4. Auto-apply integration

## Getting Help

- Check [README.md](README.md)
- Review [docs/](docs/) folder
- Check logs in `logs/jobsearch.log`
- Enable debug: `LOG_LEVEL=DEBUG`

## Cost Considerations

- **RapidAPI**: Free tiers available, check limits
- **OpenAI**: Use GPT-3.5-turbo for lower costs
- **Alternative**: Use SerpAPI for consolidated access

Estimate: ~$0.01-0.05 per job analyzed with GPT-3.5-turbo

Happy job hunting! 🚀
