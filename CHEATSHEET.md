# Job Search Agent - Quick Reference Cheatsheet

One-page reference for all common commands and workflows.

---

## 🚀 Quick Start (3 Commands)

```bash
# 1. Setup
cp .env.example .env          # Add your RAPIDAPI_KEY
python src/database/init_db.py

# 2. Test
python -m src.main --search "Python Developer" --no-analyze --limit 5

# 3. Run n8n
python src/api/server.py      # Terminal 1
n8n start                     # Terminal 2 (optional)
```

---

## 📋 Common Commands

### CLI Searches
```bash
# Basic search (no AI, save money)
python -m src.main --search "KEYWORDS" --no-analyze

# Search with AI analysis
python -m src.main --search "KEYWORDS"

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

# Search jobs
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"keywords": "Python Dev", "analyze": false}'

# Get saved jobs
curl http://localhost:5000/api/jobs?limit=10

# Filter by source
curl http://localhost:5000/api/jobs?source=indeed

# Get job by ID
curl http://localhost:5000/api/jobs/123

# Get statistics
curl http://localhost:5000/api/stats

# n8n webhook
curl -X POST http://localhost:5000/webhook/job-search \
  -H "Content-Type: application/json" \
  -d '{"keywords": "Software Engineer", "options": {"analyze": false}}'
```

---

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Required
RAPIDAPI_KEY=your_key_here

# Optional (for AI)
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
  model: "gpt-3.5-turbo"  # Or "gpt-4" for better quality
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
    "analyze": false,
    "save_to_db": true
  }
}
```

### Schedule Cron Examples
```
0 9 * * *     # 9 AM daily
0 */6 * * *   # Every 6 hours
0 9 * * 1     # 9 AM every Monday
0 9,17 * * *  # 9 AM and 5 PM daily
```

---

## 💰 Cost Optimization

### Free Setup (Zero Cost)
```bash
# 1. Use RapidAPI free tiers (100 requests/month)
# 2. Always use --no-analyze flag
# 3. Search 2-3 times per day max

python -m src.main --search "Python Dev" --no-analyze
```

### Paid Setup (Minimize Cost)
```bash
# 1. Use gpt-3.5-turbo (not gpt-4)
# 2. Analyze only top results
# 3. Filter BEFORE AI analysis

# Search without AI (fast, free)
python -m src.main --search "Python Dev" --no-analyze --limit 50

# Then manually pick top 5 and analyze with AI
# Cost: Only 5 × $0.01 = $0.05
```

### Monthly Cost Examples
```
Light (2 searches/day):
  • RapidAPI free tier: $0
  • No AI: $0
  • Total: $0/month ✅

Medium (5 searches/day):
  • RapidAPI: $20/month
  • No AI: $0
  • Total: $20/month

Heavy (10 searches/day with AI):
  • RapidAPI: $30/month
  • OpenAI: $30/month
  • Total: $60/month
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
# Use --no-analyze to skip AI
python -m src.main --search "Python" --no-analyze

# Or switch to gpt-3.5-turbo in config.yaml
model: "gpt-3.5-turbo"
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
│   ├── NO_AI_SETUP.md      ← Run without OpenAI
│   └── N8N_INTEGRATION.md  ← n8n workflows
├── WORKFLOW_DIAGRAM.md     ← Visual diagrams
└── YOUR_SETUP.md           ← Your personalized config
```

---

## 🎯 Real-World Workflows

### Daily Job Digest
```bash
# Morning: Quick search without AI
python -m src.main --search "Python Developer" --no-analyze

# Review in database
python -m src.main --list --limit 20

# Apply to interesting jobs
```

### n8n Automated Search
```
9 AM Daily:
  1. n8n triggers search
  2. Searches Indeed, Glassdoor, Monster
  3. Saves to database
  4. Sends email with count
  5. Posts to Slack
```

### Smart Filtering
```bash
# 1. Search broadly without AI (free)
python -m src.main --search "Software Engineer" --no-analyze --limit 100

# 2. Export and filter manually
python -m src.main --list --output all_jobs.json

# 3. Analyze only top matches with AI
# (Use API or CLI with analyze: true for specific jobs)
```

---

## 🔗 Useful Links

- **RapidAPI**: https://rapidapi.com/
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
- [ ] API keys added to `.env`
- [ ] Database initialized
- [ ] Platforms enabled in `config.yaml`
- [ ] Test search works
- [ ] Can list saved jobs

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
