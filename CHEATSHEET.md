# Job Search Agent - Quick Reference Cheatsheet

One-page reference for all common commands and workflows.

---

## 🚀 Quick Start (3 Commands)

```bash
# 1. Setup
cp .env.example .env          # Add your RAPIDAPI_KEY
python src/database/init_db.py

# 2. Test (AI analysis will run automatically)
python -m src.main --search "Python Developer" --limit 5

# 3. Run n8n
python src/api/server.py      # Terminal 1
n8n start                     # Terminal 2 (optional)
```

---

## 📋 Common Commands

### CLI Searches
```bash
# Basic search (AI analysis runs automatically)
python -m src.main --search "KEYWORDS"

# Search with location
python -m src.main --search "KEYWORDS" --location "City"

# Search with location
python -m src.main --search "Python Developer" --location "San Francisco"

# Limit results
python -m src.main --search "Data Scientist" --limit 10

# Export to JSON
python -m src.main --search "DevOps" --output jobs.json

# List saved jobs
python -m src.main --list --limit 20

# Filter by platform
python -m src.main --list --source indeed
python -m src.main --list --source glassdoor
python -m src.main --list --source monster
```

### API Server
```bash
# Start server
python src/api/server.py

# Different port
FLASK_PORT=8000 python src/api/server.py
```

### API Endpoints
```bash
# Health check
curl http://localhost:5000/health

# Search jobs (AI analysis runs automatically)
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"keywords": "Python Dev"}'

# Get saved jobs
curl http://localhost:5000/api/jobs?limit=10

# Filter by source
curl http://localhost:5000/api/jobs?source=indeed

# Get job by ID
curl http://localhost:5000/api/jobs/123

# Get statistics
curl http://localhost:5000/api/stats

# n8n webhook (AI analysis runs automatically)
curl -X POST http://localhost:5000/webhook/job-search \
  -H "Content-Type: application/json" \
  -d '{"keywords": "Software Engineer"}'
```

---

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Required - Job scraping
RAPIDAPI_KEY=your_key_here

# Required - AI analysis (choose ONE)
ANTHROPIC_API_KEY=your_key_here  # Recommended - 3-10x cheaper!
# OR
OPENAI_API_KEY=your_key_here

# Defaults
DATABASE_URL=sqlite:///jobs.db
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### Enable/Disable Platforms (config/config.yaml)
```yaml
scrapers:
  indeed:
    enabled: true      # ← Change to false to disable
  linkedin:
    enabled: false     # ← Already disabled
  glassdoor:
    enabled: true
  monster:
    enabled: true
```

### AI Settings (config/config.yaml)
```yaml
ai:
  provider: "anthropic"  # or "openai"
  model: "claude-3-5-sonnet-20241022"  # Recommended! Or "gpt-3.5-turbo"
  temperature: 0.7
  max_tokens: 1000
```

---

## 🔧 n8n Integration

### Start n8n
```bash
# Via npm
n8n start

# Via Docker
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n

# Access: http://localhost:5678
```

### Webhook Payload
```json
{
  "keywords": "Python Developer",
  "location": "Remote",
  "options": {
    "save_to_db": true
  }
}
```

Note: AI analysis runs automatically on all searches.

### Schedule Cron Examples
```
0 9 * * *     # 9 AM daily
0 */6 * * *   # Every 6 hours
0 9 * * 1     # 9 AM every Monday
0 9,17 * * *  # 9 AM and 5 PM daily
```

---

## 💰 Cost Optimization

### Recommended Setup (Minimize Cost)
```bash
# 1. Use Anthropic Claude (3-10x cheaper than OpenAI)
# 2. Use claude-3-5-sonnet-20241022 model
# 3. Use SerpAPI free tier (100 searches/month)

# Add to .env:
ANTHROPIC_API_KEY=your_key_here
SERPAPI_KEY=your_key_here

# Search with AI analysis
python -m src.main --search "Python Dev" --limit 50
```

### Monthly Cost Examples
```
Light (100 jobs/month):
  • SerpAPI free tier: $0
  • Anthropic Claude Sonnet: $0.30
  • Total: ~$0.30/month ✅

Medium (500 jobs/month):
  • RapidAPI: $10/month
  • Anthropic Claude Sonnet: $1.50
  • Total: ~$11.50/month

Heavy (2000 jobs/month):
  • RapidAPI: $30/month
  • Anthropic Claude Sonnet: $6
  • Total: ~$36/month

Compare to OpenAI:
  • 2000 jobs with GPT-3.5-turbo: ~$20 AI cost
  • Savings with Claude: $14/month
```

---

## 🐛 Troubleshooting

### "Module not found"
```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall
pip install -r requirements.txt
```

### "API key invalid"
```bash
# Check .env file
cat .env | grep RAPIDAPI_KEY

# Make sure no quotes or spaces
RAPIDAPI_KEY=abc123...   # ✅ Correct
RAPIDAPI_KEY="abc123..." # ❌ Wrong
```

### "No jobs found"
```bash
# Check platforms enabled
cat config/config.yaml | grep enabled

# Check API subscriptions on RapidAPI
# Verify: indeed, glassdoor, monster
```

### "Port already in use"
```bash
# Find process
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Use different port
FLASK_PORT=8000 python src/api/server.py
```

### "Database error"
```bash
# Reinitialize database
rm jobs.db  # Delete old database
python src/database/init_db.py  # Create new one
```

### "OpenAI rate limit"
```bash
# Switch to Anthropic Claude (3-10x cheaper and higher rate limits)
# Update .env:
ANTHROPIC_API_KEY=your_key_here

# Update config.yaml:
ai:
  provider: "anthropic"
  model: "claude-3-5-sonnet-20241022"
```

---

## 📁 File Structure

```
jobsearch-agent/
├── .env                    ← Your API keys
├── config/
│   ├── config.yaml         ← Main config (enable/disable platforms)
│   ├── config-free.yaml    ← Free alternatives setup
│   └── config-no-ai.yaml   ← No AI setup
├── src/
│   ├── main.py             ← CLI entry point
│   ├── api/server.py       ← API server
│   ├── database/init_db.py ← Initialize database
│   ├── scrapers/           ← Job scrapers
│   └── agents/             ← AI analysis
├── docs/
│   ├── GETTING_STARTED.md  ← Step-by-step guide
│   ├── RAPIDAPI_SETUP.md   ← RapidAPI instructions
│   ├── ANTHROPIC_SETUP.md  ← Anthropic Claude setup (recommended!)
│   └── N8N_INTEGRATION.md  ← n8n workflows
├── WORKFLOW_DIAGRAM.md     ← Visual diagrams
└── YOUR_SETUP.md           ← Your personalized config
```

---

## 🎯 Real-World Workflows

### Daily Job Digest
```bash
# Morning: Quick search with AI analysis
python -m src.main --search "Python Developer" --limit 20

# Review analyzed jobs in database
python -m src.main --list --limit 20

# Apply to interesting jobs
```

### n8n Automated Search
```
9 AM Daily:
  1. n8n triggers search
  2. Searches Indeed, Glassdoor, Monster
  3. AI analyzes all jobs automatically
  4. Saves to database with AI insights
  5. Sends email with top matches
  6. Posts to Slack
```

### Smart Filtering
```bash
# 1. Search with AI analysis
python -m src.main --search "Software Engineer" --limit 100

# 2. Export analyzed jobs
python -m src.main --list --output all_jobs.json

# 3. Review AI-extracted skills and summaries
# Jobs are already analyzed with skills, requirements, etc.
```

---

## 🔗 Useful Links

- **RapidAPI**: https://rapidapi.com/
- **Anthropic Claude**: https://console.anthropic.com/ (Recommended!)
- **OpenAI**: https://platform.openai.com/
- **n8n Docs**: https://docs.n8n.io/
- **Your Repo**: https://github.com/majidraza1228/jobsearch-agent

---

## 📞 Quick Help

```bash
# CLI help
python -m src.main --help

# Check what's running
lsof -i :5000  # API server
lsof -i :5678  # n8n

# View logs
tail -f logs/jobsearch.log

# Database stats
python -m src.main --list | head -5
```

---

## ✅ Pre-flight Checklist

Before first use:
- [ ] API keys added to `.env` (RapidAPI + Anthropic or OpenAI)
- [ ] Database initialized
- [ ] Platforms enabled in `config.yaml`
- [ ] AI provider configured in `config.yaml`
- [ ] Test search works with AI analysis
- [ ] Can list saved jobs with AI insights

Before n8n:
- [ ] API server running (port 5000)
- [ ] n8n installed and running (port 5678)
- [ ] Workflow imported
- [ ] Webhook tested

---

**Keep this page bookmarked!** 📌

For detailed guides, see:
- [GETTING_STARTED.md](docs/GETTING_STARTED.md) - Full tutorial
- [YOUR_SETUP.md](YOUR_SETUP.md) - Your specific config
- [WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md) - Visual flows
