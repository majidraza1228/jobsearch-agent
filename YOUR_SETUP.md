# Your Custom Setup Configuration

This document describes your specific configuration without LinkedIn.

## Active Job Platforms

✅ **Indeed** - Enabled
✅ **Glassdoor** - Enabled
✅ **Monster** - Enabled
❌ **LinkedIn** - Disabled (can be enabled later if needed)

## What You Need

### 1. RapidAPI Subscriptions (Required)

You only need to subscribe to **3 APIs** on RapidAPI:

1. ✅ **Indeed Jobs API**
   - Search: https://rapidapi.com/search/indeed%20jobs
   - Recommended: "Indeed Jobs Search API"
   - Free tier: Usually 100 requests/month

2. ✅ **Glassdoor Jobs API**
   - Search: https://rapidapi.com/search/glassdoor%20jobs
   - Recommended: "Glassdoor Job Search API"
   - Pricing varies by provider

3. ✅ **Monster Jobs API**
   - Search: https://rapidapi.com/search/monster%20jobs
   - Recommended: "Monster Job Search API"
   - Pricing varies by provider

**You do NOT need LinkedIn API** - it's disabled in your config!

### 2. OpenAI API Key (Optional but Recommended)

- Sign up: https://platform.openai.com/
- Cost: ~$0.01 per job analyzed (using GPT-3.5-turbo)
- For 100 jobs analyzed = ~$1
- Can skip with `--no-analyze` flag to save cost

## Setup Steps

### Step 1: Get RapidAPI Key

1. Go to https://rapidapi.com/ and sign up
2. Subscribe to Indeed, Glassdoor, and Monster APIs (start with free tiers)
3. Copy your RapidAPI key (one key for all APIs!)

### Step 2: Configure Environment

```bash
# Copy example file
cp .env.example .env

# Edit .env file
nano .env  # or use your favorite editor
```

Add your keys:
```env
# Only these two are needed!
RAPIDAPI_KEY=your_rapidapi_key_here
OPENAI_API_KEY=your_openai_key_here
```

### Step 3: Initialize Database

```bash
python src/database/init_db.py
```

### Step 4: Test Your Setup

```bash
# Search for jobs
python -m src.main --search "Software Engineer" --location "Remote" --limit 10

# Expected output: Jobs from Indeed, Glassdoor, and Monster
# LinkedIn will be skipped (disabled)
```

## Usage Examples

### Basic Search
```bash
python -m src.main --search "Python Developer" --location "San Francisco"
```

### Search Without AI Analysis (Save Money)
```bash
python -m src.main --search "Data Scientist" --no-analyze
```

### List Saved Jobs
```bash
python -m src.main --list --limit 20
```

### Filter by Platform
```bash
# Indeed only
python -m src.main --list --source indeed

# Glassdoor only
python -m src.main --list --source glassdoor

# Monster only
python -m src.main --list --source monster
```

### Export to JSON
```bash
python -m src.main --search "DevOps Engineer" --output jobs.json
```

### Start API Server (for n8n)
```bash
python src/api/server.py
# Server runs on http://localhost:5000
```

## Cost Estimation (Monthly)

### Light Usage (100 searches/month)
- RapidAPI: $0 (free tiers)
- OpenAI: ~$1 (100 jobs × $0.01)
- **Total: ~$1/month**

### Medium Usage (500 searches/month)
- RapidAPI: ~$10-20 (basic paid plans)
- OpenAI: ~$5 (500 jobs × $0.01)
- **Total: ~$15-25/month**

### Heavy Usage (2000 searches/month)
- RapidAPI: ~$30-50 (pro plans)
- OpenAI: ~$20 (2000 jobs × $0.01)
- **Total: ~$50-70/month**

## Enabling LinkedIn Later

If you want to add LinkedIn later:

1. Subscribe to LinkedIn API on RapidAPI
2. Edit `config/config.yaml`:
   ```yaml
   linkedin:
     enabled: true  # Change from false to true
   ```
3. Restart the application

## n8n Integration

Your webhook endpoint: `http://localhost:5000/webhook/job-search`

Example request:
```json
{
  "keywords": "Software Engineer",
  "location": "Remote",
  "options": {
    "analyze": true,
    "save_to_db": true
  }
}
```

Expected response includes jobs from: **Indeed + Glassdoor + Monster**

## Troubleshooting

### No Jobs from LinkedIn
✅ **This is normal!** LinkedIn is disabled in your configuration.

### Only Getting Results from 1-2 Platforms
- Check RapidAPI subscriptions are active
- Verify API endpoints in `config/config.yaml`
- Check API rate limits

### OpenAI Costs Too High
- Use `--no-analyze` flag to skip AI analysis
- Or switch to analyzing only top matches
- Free alternative: Just save job data without AI

## Quick Commands Reference

```bash
# Setup
cp .env.example .env          # Create environment file
python src/database/init_db.py  # Initialize database

# Search
python -m src.main --search "KEYWORDS" --location "LOCATION"

# List jobs
python -m src.main --list --limit 20

# API server
python src/api/server.py

# Help
python -m src.main --help
```

## Your Configuration Summary

- **Platforms**: Indeed, Glassdoor, Monster (3 platforms)
- **AI Model**: GPT-3.5-turbo (cost-effective)
- **Database**: SQLite (local storage)
- **API Server**: Flask on port 5000
- **n8n Ready**: Yes, webhook configured

## Support

- Full documentation: `docs/` folder
- RapidAPI setup: `docs/RAPIDAPI_SETUP.md`
- n8n integration: `docs/N8N_INTEGRATION.md`
- Quick start: `QUICK_START.md`

Happy job hunting! 🚀
