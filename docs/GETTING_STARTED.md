# Getting Started: Local Testing → n8n Integration

Complete step-by-step guide from local testing to n8n orchestration.

---

## Part 1: Local Testing (30 minutes)

### Step 1: Get Your API Keys (10 min)

#### A. RapidAPI Key (Required)

1. Go to https://rapidapi.com/
2. Click "Sign Up" (top right)
3. Sign up with Google or email
4. Once logged in, search for and subscribe to these APIs:
   - **Indeed Jobs API** - https://rapidapi.com/search/indeed%20jobs
   - **Glassdoor Jobs API** - https://rapidapi.com/search/glassdoor%20jobs
   - **Monster Jobs API** - https://rapidapi.com/search/monster%20jobs
5. For each API, click "Subscribe to Test" and choose:
   - **Basic (Free)** tier to start (100 requests/month)
   - Or **Paid** tier if you need more
6. Get your API key:
   - Go to any subscribed API
   - Look for **"X-RapidAPI-Key"** in the code snippets
   - Copy this key (it's the SAME for all APIs)

#### B. OpenAI Key (Optional - for AI analysis)

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Click "API Keys" in the left menu
4. Click "Create new secret key"
5. Copy the key (starts with `sk-proj-...`)
6. **Save it now** - you can't see it again!

> **Skip OpenAI** if you want to test for free first. You can add it later.

---

### Step 2: Install the Project (5 min)

```bash
# Navigate to project folder
cd /Users/syedraza/jobsearch-agent

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

You should see packages installing (Flask, SQLAlchemy, etc.)

---

### Step 3: Configure API Keys (5 min)

```bash
# Create .env file from example
cp .env.example .env

# Open .env file
nano .env   # or use any text editor
```

Add your keys:

```env
# ============================================
# REQUIRED: Add your RapidAPI key here
# ============================================
RAPIDAPI_KEY=paste_your_rapidapi_key_here

# ============================================
# OPTIONAL: Add OpenAI key (or leave empty)
# ============================================
OPENAI_API_KEY=paste_your_openai_key_here

# ============================================
# Leave everything else as default
# ============================================
DATABASE_URL=sqlite:///jobs.db
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_ENV=development
```

**Save and close** (Ctrl+X, then Y, then Enter in nano)

---

### Step 4: Initialize Database (1 min)

```bash
python src/database/init_db.py
```

Expected output:
```
Initializing database...
Database tables created successfully.
Database initialization complete!
```

---

### Step 5: Test Search (CLI) (5 min)

Now let's test if everything works!

#### Test WITHOUT OpenAI (Free):
```bash
python -m src.main --search "Python Developer" --location "Remote" --no-analyze --limit 5
```

#### Test WITH OpenAI (if you added the key):
```bash
python -m src.main --search "Python Developer" --location "Remote" --limit 5
```

**Expected output:**
```
================================================================================
Search Results: Python Developer
Location: Remote
================================================================================

Total jobs found: 15
New jobs saved: 15

Platform breakdown:
  - indeed: 5
  - glassdoor: 5
  - monster: 5

================================================================================
Job Listings:
================================================================================

1. Senior Python Developer at Tech Corp
   Source: indeed | Location: Remote
   URL: https://indeed.com/viewjob?jk=abc123
   AI Summary: Looking for experienced Python developer... (if AI enabled)

2. Python Software Engineer at StartupXYZ
   Source: glassdoor | Location: Remote, USA
   URL: https://glassdoor.com/job/...
   ...
```

✅ **If you see jobs, it's working!**

---

### Step 6: Test Listing Jobs (2 min)

```bash
# List all saved jobs
python -m src.main --list --limit 10

# List only Indeed jobs
python -m src.main --list --source indeed

# List only Glassdoor jobs
python -m src.main --list --source glassdoor
```

---

### Step 7: Start API Server (2 min)

```bash
python src/api/server.py
```

Expected output:
```
Starting Flask server on 0.0.0.0:5000
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

**Keep this running** in this terminal window!

---

### Step 8: Test API (in a NEW terminal)

Open a **new terminal window** and test:

```bash
# Test health check
curl http://localhost:5000/health

# Expected: {"status":"healthy","service":"job-search-agent"}

# Test job search
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Software Engineer",
    "location": "San Francisco",
    "analyze": false
  }'

# Test get jobs
curl http://localhost:5000/api/jobs?limit=5

# Test stats
curl http://localhost:5000/api/stats
```

✅ **If you get JSON responses, the API is working!**

---

## Part 2: n8n Integration (45 minutes)

### Step 1: Install n8n (10 min)

#### Option A: Using npm (Recommended)
```bash
# Install n8n globally
npm install -g n8n

# Start n8n
n8n start
```

#### Option B: Using Docker
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

n8n will start on: **http://localhost:5678**

---

### Step 2: Access n8n (2 min)

1. Open browser: http://localhost:5678
2. Create account (first time only)
3. You'll see the n8n dashboard

---

### Step 3: Import Workflow (5 min)

1. In n8n, click **"Add workflow"** (top right)
2. Click the **three dots menu** (⋮) → **"Import from File"**
3. Navigate to: `/Users/syedraza/jobsearch-agent/n8n-workflows/job-search-workflow.json`
4. Click **"Import"**
5. The workflow will appear with all nodes

---

### Step 4: Configure Workflow (10 min)

#### A. Update API Endpoint

1. Click on the **"Call Job Search Agent"** HTTP Request node
2. In the settings, verify URL is: `http://localhost:5000/webhook/job-search`
3. If your API server runs on a different port, update it

#### B. Configure Webhook Trigger

1. Click on the **"Webhook"** node
2. Note the webhook URL (something like `http://localhost:5678/webhook/job-search`)
3. Click **"Listen for Test Event"** or **"Execute Node"**

---

### Step 5: Test the Workflow (10 min)

#### Method A: Trigger via Webhook

In a terminal:

```bash
curl -X POST http://localhost:5678/webhook/job-search \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Data Scientist",
    "location": "New York",
    "options": {
      "analyze": false,
      "save_to_db": true
    }
  }'
```

#### Method B: Use Manual Trigger in n8n

1. In n8n, click **"Test workflow"** (top right)
2. Click on the **Webhook node**
3. Click **"Execute Node"**
4. The workflow should run

**Expected result:**
- Webhook receives request
- HTTP node calls your API
- Response shows job results
- Jobs are saved to database

---

### Step 6: Set Up Scheduled Searches (5 min)

1. In the workflow, find the **"Schedule (Optional)"** node
2. **Enable it** (toggle switch)
3. Configure the schedule:
   - Click on the node
   - Set **Cron Expression**: `0 9 * * *` (runs at 9 AM daily)
   - Or use the **interval** option

4. Find the **"Set Search Parameters"** node
5. **Enable it**
6. Click on it and configure:
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

7. Click **"Save"** (top right)
8. Click **"Activate"** (top right toggle)

Now it runs automatically every day at 9 AM! ⏰

---

### Step 7: Add Notifications (Optional - 3 min)

#### A. Email Notifications

1. Find the **"Send Email Notification"** node
2. **Enable it**
3. Configure your email settings:
   - From Email: `your-email@gmail.com`
   - To Email: `your-email@gmail.com`
   - Subject: `New Jobs Found!`
4. Configure SMTP in n8n settings (Gmail, SendGrid, etc.)

#### B. Slack Notifications

1. Add a **Slack node** to the workflow
2. Connect it after "Process Jobs"
3. Configure Slack credentials
4. Set message template:
   ```
   🎯 Found {{ $json.data.total_jobs }} new jobs!

   Indeed: {{ $json.data.platform_breakdown.indeed }}
   Glassdoor: {{ $json.data.platform_breakdown.glassdoor }}
   Monster: {{ $json.data.platform_breakdown.monster }}
   ```

---

## Part 3: Real-World Usage Examples

### Example 1: Daily Job Digest

**Setup:**
1. Schedule trigger: 9 AM daily
2. Search: "Software Engineer" in "Remote"
3. Save to database
4. Send email with results

**n8n Configuration:**
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

---

### Example 2: Multi-Keyword Search

Search for multiple job types:

**Workflow:**
1. Trigger: Webhook or Schedule
2. Loop through keywords: ["Python Dev", "Data Scientist", "ML Engineer"]
3. For each keyword, call job search API
4. Aggregate results
5. Send report

---

### Example 3: Smart Job Filtering

**Workflow:**
1. Search for jobs (without AI to save money)
2. Filter by keywords in description (use n8n Function node):
   ```javascript
   const jobs = items[0].json.data.jobs;
   const filtered = jobs.filter(job =>
     job.description.includes('remote') &&
     job.description.includes('senior')
   );
   return [{ json: { jobs: filtered } }];
   ```
3. Only analyze filtered jobs with AI (save money!)
4. Send top matches via email

---

### Example 4: Job Application Tracker

**Workflow:**
1. Search for jobs
2. Save to Google Sheets or Airtable
3. Add columns: "Applied", "Status", "Follow-up Date"
4. Set up reminder notifications

---

## Troubleshooting

### Issue: "Connection refused" when calling API

**Solution:**
1. Make sure API server is running:
   ```bash
   python src/api/server.py
   ```
2. Check it's on correct port (5000)
3. Test with: `curl http://localhost:5000/health`

---

### Issue: No jobs returned

**Solution:**
1. Check RapidAPI subscriptions are active
2. Verify API key in `.env`
3. Check platform is enabled in `config/config.yaml`
4. Look at API server logs for errors

---

### Issue: OpenAI errors

**Solution:**
1. Check API key is valid
2. Check OpenAI billing/credits
3. Or use `--no-analyze` flag to skip AI

---

### Issue: n8n workflow fails

**Solution:**
1. Check both servers are running (API + n8n)
2. Verify webhook URL is correct
3. Check JSON format in request
4. Look at n8n execution logs

---

## Quick Reference Commands

```bash
# ============================================
# LOCAL TESTING
# ============================================

# Search without AI (free)
python -m src.main --search "KEYWORD" --no-analyze

# Search with AI
python -m src.main --search "KEYWORD"

# List jobs
python -m src.main --list --limit 20

# Start API server
python src/api/server.py

# Test API
curl http://localhost:5000/health

# ============================================
# N8N
# ============================================

# Start n8n
n8n start

# Access n8n
# Browser: http://localhost:5678

# Test webhook
curl -X POST http://localhost:5678/webhook/job-search \
  -H "Content-Type: application/json" \
  -d '{"keywords": "Python Dev", "options": {"analyze": false}}'
```

---

## Summary Checklist

### ✅ Local Testing
- [ ] API keys obtained (RapidAPI + OpenAI optional)
- [ ] `.env` file configured
- [ ] Database initialized
- [ ] CLI search works
- [ ] API server starts
- [ ] API endpoints respond

### ✅ n8n Integration
- [ ] n8n installed and running
- [ ] Workflow imported
- [ ] HTTP node configured
- [ ] Webhook tested
- [ ] Schedule configured (optional)
- [ ] Notifications set up (optional)

### ✅ Production Ready
- [ ] Scheduled searches active
- [ ] Email/Slack notifications working
- [ ] Database backing up regularly
- [ ] Monitoring API usage/costs

---

## Next Steps

1. **Start simple**: Use CLI for a few days
2. **Add API**: Start the server, test endpoints
3. **Integrate n8n**: Import workflow, test webhook
4. **Automate**: Set up scheduled searches
5. **Enhance**: Add filters, notifications, integrations

**You're all set! 🚀 Happy job hunting!**

For more help:
- [YOUR_SETUP.md](../YOUR_SETUP.md) - Your personalized config
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
- [N8N_INTEGRATION.md](N8N_INTEGRATION.md) - Advanced n8n setups
