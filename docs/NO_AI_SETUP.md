# Setup Without OpenAI (No AI Analysis)

Complete guide to running the Job Search Agent **WITHOUT OpenAI** to save money.

## What You Get Without OpenAI

### ✅ Full Job Data
- Job title
- Company name
- Location
- Complete job description
- Job URL (link to apply)
- Posted date
- Job type (full-time, part-time, contract)
- Salary information (if mentioned in posting)
- All raw data from job boards

### ✅ Full Functionality
- Search across Indeed, Glassdoor, Monster
- Save jobs to SQLite database
- n8n webhook integration
- REST API access
- CLI interface
- Export to JSON

### ❌ What You DON'T Get
- AI-extracted skills list
- AI-generated job summaries
- AI job matching scores
- Structured skill extraction
- Experience level parsing

## Cost Comparison

| Setup | Monthly Cost |
|-------|-------------|
| **With OpenAI** | RapidAPI ($10-30) + OpenAI ($1-20) = **$11-50/month** |
| **Without OpenAI** | RapidAPI only ($10-30) = **$10-30/month** |
| **Without OpenAI (Free tier)** | RapidAPI free tiers = **$0/month** |

## Setup Instructions

### Step 1: Configure Environment

Create `.env` file with **ONLY** RapidAPI key:

```bash
cp .env.example .env
```

Edit `.env`:
```env
# ONLY THIS IS REQUIRED
RAPIDAPI_KEY=your_rapidapi_key_here

# Leave OpenAI commented out or empty
# OPENAI_API_KEY=

# Database
DATABASE_URL=sqlite:///jobs.db

# API Server
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_ENV=development
```

### Step 2: Initialize Database

```bash
python src/database/init_db.py
```

### Step 3: Search Jobs WITHOUT AI Analysis

```bash
# Use --no-analyze flag to skip AI analysis
python -m src.main --search "Software Engineer" --location "Remote" --no-analyze
```

## Usage Examples

### Search Without AI
```bash
python -m src.main --search "Python Developer" --no-analyze
```

### Search and Save Without AI
```bash
python -m src.main --search "Data Scientist" --location "San Francisco" --no-analyze
```

### List Saved Jobs
```bash
python -m src.main --list --limit 20
```

### Export to JSON
```bash
python -m src.main --search "DevOps Engineer" --no-analyze --output jobs.json
```

## API Usage Without OpenAI

### Start Server
```bash
python src/api/server.py
```

### Search Jobs via API
```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Software Engineer",
    "location": "Remote",
    "analyze": false
  }'
```

Note: Set `"analyze": false` in API requests!

## n8n Integration Without AI

Update your n8n webhook payload:

```json
{
  "keywords": "Software Engineer",
  "location": "Remote",
  "options": {
    "analyze": false,
    "save_to_db": true
  }
}
```

## What Job Data Looks Like

### Without OpenAI (Raw Data)
```json
{
  "id": 1,
  "title": "Senior Python Developer",
  "company": "Tech Corp",
  "location": "Remote",
  "description": "We are seeking an experienced Python developer with 5+ years...",
  "url": "https://indeed.com/job/12345",
  "job_type": "full-time",
  "remote_type": "remote",
  "posted_date": "2025-01-01",
  "source": "indeed"
}
```

### With OpenAI (Enhanced Data)
```json
{
  "id": 1,
  "title": "Senior Python Developer",
  "company": "Tech Corp",
  "location": "Remote",
  "description": "We are seeking an experienced Python developer with 5+ years...",
  "url": "https://indeed.com/job/12345",
  "job_type": "full-time",
  "remote_type": "remote",
  "posted_date": "2025-01-01",
  "source": "indeed",
  "ai_extracted_skills": ["Python", "Django", "AWS", "Docker"],
  "ai_summary": "Senior role requiring 5+ years Python experience...",
  "required_experience_years": 5,
  "match_score": 85.5
}
```

## Benefits of No AI Setup

### ✅ Advantages
1. **Lower cost** - Save $1-20/month on OpenAI
2. **Faster** - No AI processing delay
3. **Simpler** - One less API key to manage
4. **Privacy** - Job data not sent to OpenAI

### ⚠️ Limitations
1. No automated skill extraction
2. No job summaries
3. No matching scores
4. Must manually read descriptions

## When to Add OpenAI Later

Consider adding OpenAI if you:
- Search for 100+ jobs and need quick summaries
- Want automated skill extraction
- Need job matching against your profile
- Can afford ~$1-20/month extra

To enable AI later:
1. Get OpenAI API key from https://platform.openai.com/
2. Add to `.env`: `OPENAI_API_KEY=sk-...`
3. Remove `--no-analyze` flag from commands
4. Or set `"analyze": true` in API/n8n requests

## Alternative: Manual Analysis

You can do your own analysis:
1. Save jobs without AI
2. Export to JSON or CSV
3. Use your own tools to analyze
4. Or manually review job descriptions

## Recommended Setup (No AI)

For personal job searching without AI:

1. **Use RapidAPI free tiers**:
   - Indeed: 100 requests/month free
   - Glassdoor: Varies
   - Monster: Varies

2. **Search 2-3 times per day**:
   ```bash
   # Morning search
   python -m src.main --search "Software Engineer" --no-analyze

   # Evening search
   python -m src.main --search "Python Developer" --no-analyze
   ```

3. **Review saved jobs**:
   ```bash
   python -m src.main --list --limit 50
   ```

4. **Total cost**: **$0/month** (using free tiers)

## Troubleshooting

### Error: "OpenAI API key not found"
✅ **This is fine!** Just use `--no-analyze` flag.

### Jobs saved without AI fields
✅ **This is expected!** Fields like `ai_summary` and `ai_extracted_skills` will be null/empty.

### Can I enable AI for some searches?
✅ **Yes!** Just omit `--no-analyze` when you want AI analysis (requires OpenAI key).

## Summary

**You DON'T need OpenAI if:**
- You're okay reading job descriptions manually
- You want to minimize costs
- You prefer privacy (no data sent to OpenAI)
- You'll do your own analysis

**The job search agent works perfectly fine without OpenAI!**

Just remember to use the `--no-analyze` flag:
```bash
python -m src.main --search "YOUR SEARCH" --no-analyze
```

Happy job hunting! 🚀 (No AI required!)
