# Job Search AI Agent for n8n

An intelligent job search agent that scrapes job requirements from multiple platforms (Indeed, LinkedIn, Glassdoor, Monster) and integrates seamlessly with n8n workflows.

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/majidraza1228/jobsearch-agent)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## ✨ Features

- 🔍 **Multi-platform job scraping** - Indeed, LinkedIn, Glassdoor, Monster
- 🤖 **AI-powered analysis** - Extract skills, requirements, and summaries with OpenAI
- 📊 **SQLite database** - Automatic job storage and deduplication
- 🔗 **n8n integration** - Webhook support for workflow automation
- 🌐 **API-based scraping** - Reliable, legal access via RapidAPI
- ⚡ **RESTful API** - Complete API for custom integrations
- 💰 **Flexible pricing** - Free tier available, optional AI features
- 🎯 **Smart filtering** - Search by keywords, location, job type

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Documentation](#-documentation)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage Examples](#-usage-examples)
- [API Reference](#-api-reference)
- [Configuration](#-configuration)
- [Cost Guide](#-cost-guide)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

Get up and running in 3 commands:

```bash
# 1. Setup environment
cp .env.example .env  # Add your RAPIDAPI_KEY
python src/database/init_db.py

# 2. Test search (no AI, free)
python -m src.main --search "Python Developer" --no-analyze --limit 5

# 3. Start API server (for n8n)
python src/api/server.py
```

**See [GETTING_STARTED.md](docs/GETTING_STARTED.md) for detailed step-by-step instructions.**

---

## 📚 Documentation

### 🎯 Getting Started
- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** - Complete tutorial from local testing to n8n integration (START HERE!)
- **[CHEATSHEET.md](CHEATSHEET.md)** - Quick reference for all commands and common tasks
- **[WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md)** - Visual diagrams showing how everything works
- **[QUICK_START.md](QUICK_START.md)** - 5-minute overview and setup

### ⚙️ Setup Guides
- **[YOUR_SETUP.md](YOUR_SETUP.md)** - Personalized configuration (Indeed + Glassdoor + Monster, no LinkedIn)
- **[RAPIDAPI_SETUP.md](docs/RAPIDAPI_SETUP.md)** - How to get and configure RapidAPI keys
- **[ANTHROPIC_SETUP.md](docs/ANTHROPIC_SETUP.md)** - Use Anthropic Claude (3-10x cheaper than OpenAI!)
- **[ALTERNATIVE_APIS.md](docs/ALTERNATIVE_APIS.md)** - Free alternatives: SerpAPI, Adzuna, RSS feeds

### 📖 Reference Documentation
- **[API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)** - Complete REST API reference with examples
- **[N8N_INTEGRATION.md](docs/N8N_INTEGRATION.md)** - Advanced n8n workflows and integrations
- **[SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** - Comprehensive installation and configuration guide

### 📁 Configuration Files
- **[config.yaml](config/config.yaml)** - Main configuration (enabled platforms, AI settings)
- **[config-free.yaml](config/config-free.yaml)** - Configuration using only free APIs
- **[config-no-ai.yaml](config/config-no-ai.yaml)** - Configuration without AI analysis

---

## 🔑 Prerequisites

### Required
- **Python 3.9+**
- **API Keys** - Choose one option:

  | Option | Cost | Searches/Month | Best For |
  |--------|------|----------------|----------|
  | **RapidAPI** | $0-50/mo | 100-5000+ | Most reliable, recommended |
  | **SerpAPI** | FREE tier | 100 free | Best free option |
  | **Adzuna** | FREE | 250 free | UK/Europe jobs |

  📖 See [RAPIDAPI_SETUP.md](docs/RAPIDAPI_SETUP.md) for RapidAPI setup
  📖 See [ALTERNATIVE_APIS.md](docs/ALTERNATIVE_APIS.md) for free options

### Required (AI Analysis)
- **Choose ONE AI provider** for job analysis:

  | Provider | Cost/Job | Models | Best For |
  |----------|----------|--------|----------|
  | **Anthropic Claude** | $0.0005-0.015 | Haiku, Sonnet, Opus | **Best value!** |
  | **OpenAI GPT** | $0.01-0.05 | GPT-3.5, GPT-4 | Industry standard |

  - ✅ Extracts skills, requirements, summaries
  - ✅ **Anthropic is 3-10x cheaper** than OpenAI!
  - ⚠️ AI analysis is **REQUIRED** - you must have at least one API key
  - 📖 [ANTHROPIC_SETUP.md](docs/ANTHROPIC_SETUP.md) - Claude setup (recommended!)

---

## 📦 Installation

```bash
# 1. Clone the repository
git clone https://github.com/majidraza1228/jobsearch-agent.git
cd jobsearch-agent

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
nano .env  # Add your RAPIDAPI_KEY and optionally OPENAI_API_KEY

# 5. Initialize database
python src/database/init_db.py
```

**For detailed instructions, see [GETTING_STARTED.md](docs/GETTING_STARTED.md)**

---

## 💡 Usage Examples

### Command Line Interface

```bash
# Basic search with AI analysis
python -m src.main --search "Python Developer" --location "Remote"

# Search with location
python -m src.main --search "Data Scientist" --location "New York"

# List saved jobs
python -m src.main --list --limit 20

# Filter by platform
python -m src.main --list --source indeed

# Export to JSON
python -m src.main --search "DevOps Engineer" --output jobs.json
```

### API Server

```bash
# Start the API server
python src/api/server.py

# In another terminal, test the API
curl http://localhost:5000/health

# Search for jobs (AI analysis runs automatically)
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"keywords": "Software Engineer"}'
```

### n8n Integration

1. Start the API server: `python src/api/server.py`
2. Import workflow: `n8n-workflows/job-search-workflow.json`
3. Configure webhook URL: `http://localhost:5000/webhook/job-search`
4. Set up scheduled searches

**Full n8n guide: [N8N_INTEGRATION.md](docs/N8N_INTEGRATION.md)**

---

## 🔌 API Reference

### Main Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/search` | POST | Search for jobs across platforms |
| `/api/jobs` | GET | Retrieve saved jobs from database |
| `/api/jobs/{id}` | GET | Get specific job by ID |
| `/webhook/job-search` | POST | n8n webhook endpoint |
| `/api/analyze` | POST | Analyze job description with AI |
| `/api/stats` | GET | Get database statistics |

**Complete API documentation: [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)**

---

## ⚙️ Configuration

### Enable/Disable Platforms

Edit `config/config.yaml`:

```yaml
scrapers:
  indeed:
    enabled: true      # Enable/disable Indeed
  linkedin:
    enabled: false     # Currently disabled
  glassdoor:
    enabled: true      # Enable/disable Glassdoor
  monster:
    enabled: true      # Enable/disable Monster
```

### AI Settings

```yaml
ai:
  model: "gpt-3.5-turbo"  # Or "gpt-4" for better quality
  temperature: 0.7
  max_tokens: 1000
```

**See [Configuration Files](#-configuration-files) for pre-made configs**

---

## 💰 Cost Guide

### Light Usage (~$1-2/month)
- RapidAPI free tier or SerpAPI (100 requests/month)
- AI analysis with Anthropic Claude Sonnet
- Analyze ~100 jobs/month
- **Total: ~$1-2/month** ✅

### Medium Usage (~$5-10/month)
- RapidAPI or SerpAPI
- AI analysis with Anthropic Claude Sonnet
- Analyze ~500 jobs/month
- **Total: ~$5-10/month**

### Heavy Usage (~$20-30/month)
- RapidAPI paid plans: $10-20/month
- AI with Anthropic Claude: $5-10/month
- 1000+ searches per month
- **Total: ~$20-30/month**

**Detailed cost breakdown: [ALTERNATIVE_APIS.md](docs/ALTERNATIVE_APIS.md)**

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Module not found" | Activate virtual environment: `source venv/bin/activate` |
| "API key invalid" | Check `.env` file, ensure no quotes around key |
| "No jobs found" | Verify platforms enabled in `config/config.yaml` |
| "Port already in use" | Use different port: `FLASK_PORT=8000 python src/api/server.py` |
| "Database error" | Reinitialize: `python src/database/init_db.py` |

**Full troubleshooting guide: [GETTING_STARTED.md](docs/GETTING_STARTED.md#troubleshooting)**

**Quick reference: [CHEATSHEET.md](CHEATSHEET.md#-troubleshooting)**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│  Job Platforms (APIs)                       │
│  ├─ Indeed (RapidAPI)                       │
│  ├─ Glassdoor (RapidAPI)                    │
│  └─ Monster (RapidAPI)                      │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  Job Search Agent (Python/Flask)            │
│  ├─ Scrapers (normalize job data)           │
│  ├─ AI Analyzer (OpenAI - optional)         │
│  ├─ Database (SQLite)                       │
│  └─ REST API (Flask)                        │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  Integrations                               │
│  ├─ CLI (terminal)                          │
│  ├─ n8n (automation)                        │
│  ├─ Webhook (HTTP)                          │
│  └─ Custom integrations (API)               │
└─────────────────────────────────────────────┘
```

**Visual diagrams: [WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md)**

---

## 📂 Project Structure

```
jobsearch-agent/
├── src/
│   ├── scrapers/          # Job scrapers (Indeed, LinkedIn, Glassdoor, Monster, SerpAPI, Adzuna)
│   ├── agents/            # AI job analyzer and orchestration
│   ├── database/          # SQLite models and connection
│   ├── api/               # Flask REST API server
│   ├── utils/             # Configuration and logging utilities
│   └── main.py            # CLI entry point
├── config/
│   ├── config.yaml        # Main configuration
│   ├── config-free.yaml   # Free APIs only
│   └── config-no-ai.yaml  # Without AI analysis
├── docs/                  # All documentation
├── n8n-workflows/         # n8n workflow templates
├── .env.example           # Environment variables template
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🌟 Star This Repository!

If you find this project helpful, please give it a star ⭐ on [GitHub](https://github.com/majidraza1228/jobsearch-agent)!

---

## 📞 Support

- 📖 **Documentation**: Check the `docs/` folder
- 🐛 **Issues**: [GitHub Issues](https://github.com/majidraza1228/jobsearch-agent/issues)
- 💬 **Questions**: See [GETTING_STARTED.md](docs/GETTING_STARTED.md) for FAQs

---

## 🎯 Quick Links

- [🚀 Getting Started](docs/GETTING_STARTED.md) - Start here!
- [📝 Cheatsheet](CHEATSHEET.md) - Quick reference
- [🔧 API Docs](docs/API_DOCUMENTATION.md) - API reference
- [🔗 n8n Guide](docs/N8N_INTEGRATION.md) - Automation workflows
- [💰 Cost Guide](docs/ANTHROPIC_SETUP.md) - Cheapest AI setup with Anthropic

---

**Built with ❤️ using Python, Flask, OpenAI, and n8n**

🤖 *Generated with [Claude Code](https://claude.com/claude-code)*
