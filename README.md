# Job Search AI Agent for n8n

An intelligent job search agent that scrapes job requirements from multiple platforms (Indeed, LinkedIn, Glassdoor, Monster) and integrates seamlessly with n8n workflows.

## Features

- 🔍 Multi-platform job scraping (Indeed, LinkedIn, Glassdoor, Monster)
- 🤖 AI-powered job matching and analysis
- 📊 SQLite database for job storage
- 🔗 n8n webhook integration
- 🌐 API-based scraping for reliability
- ⚡ RESTful API endpoints

## Architecture

```
jobsearch-agent/
├── src/
│   ├── scrapers/          # Job scraper modules
│   ├── database/          # Database models and setup
│   ├── api/               # Flask API endpoints
│   ├── agents/            # AI agent logic
│   └── utils/             # Helper functions
├── n8n-workflows/         # n8n workflow templates
├── config/                # Configuration files
└── tests/                 # Unit tests
```

## Prerequisites

- Python 3.9+
- API Keys (choose one option):
  - **Option 1 (Paid)**: RapidAPI key - $10-50/month ([Setup Guide](docs/RAPIDAPI_SETUP.md))
  - **Option 2 (Free)**: SerpAPI key - 100 free searches/month ([Sign up](https://serpapi.com/))
  - **Option 3 (Free)**: Adzuna API - 250 free calls/month ([Sign up](https://developer.adzuna.com/))
- OpenAI API key (optional, for AI analysis) - ~$0.01/job with GPT-3.5-turbo

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```
4. Initialize the database:
   ```bash
   python src/database/init_db.py
   ```

## Usage

### Standalone Mode
```bash
python src/main.py --search "Python Developer" --location "Remote"
```

### API Server Mode (for n8n)
```bash
python src/api/server.py
```

### n8n Integration
1. Import the workflow from `n8n-workflows/job-search-workflow.json`
2. Configure webhook URL to point to your API server
3. Set up scheduled triggers as needed

## API Endpoints

- `POST /api/search` - Search for jobs
- `GET /api/jobs` - Retrieve stored jobs
- `GET /api/jobs/{id}` - Get specific job details
- `POST /api/analyze` - Analyze job requirements with AI

## Configuration

Edit `config/config.yaml` to customize:
- Search parameters (keywords, locations)
- Scraping frequency
- Database settings
- AI model preferences

## License

MIT
