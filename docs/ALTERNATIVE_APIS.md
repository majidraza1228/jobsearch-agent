# Alternative API Options

This document outlines alternatives to RapidAPI for job searching.

## Option 1: Official Job Board APIs

### LinkedIn Jobs API
- **Official**: LinkedIn Talent Solutions API
- **Cost**: Enterprise only (very expensive)
- **Free alternative**: Use Google Jobs API for LinkedIn listings

### Indeed API
- **Official**: Indeed Publisher API
- **URL**: https://opensource.indeedeng.io/api-documentation/
- **Cost**: Free with publisher account
- **Limitations**: Must display Indeed branding

### Glassdoor API
- **Official**: Glassdoor API
- **Cost**: Enterprise only
- **Alternative**: Use web scraping (not recommended)

### Monster API
- **Official**: No public API
- **Alternative**: RSS feeds or web scraping

## Option 2: SerpAPI (Recommended Alternative)

**Best alternative to RapidAPI** - Get Google Jobs results from all platforms.

### Setup
```bash
# Sign up at https://serpapi.com/
# Get API key
# Add to .env
SERPAPI_KEY=your_serpapi_key
```

### Pricing
- Free: 100 searches/month
- Paid: From $50/month for 5,000 searches

### Advantages
- ✅ Aggregates all job platforms (Indeed, LinkedIn, Glassdoor, etc.)
- ✅ Google Jobs integration
- ✅ Reliable and legal
- ✅ Better free tier than individual APIs

### Usage Example
```python
import requests

params = {
    "api_key": "YOUR_SERPAPI_KEY",
    "engine": "google_jobs",
    "q": "Python Developer",
    "location": "Remote"
}

response = requests.get("https://serpapi.com/search", params=params)
jobs = response.json()["jobs_results"]
```

## Option 3: Free Job APIs

### 1. Adzuna API
- **URL**: https://developer.adzuna.com/
- **Cost**: Free tier available
- **Coverage**: UK, US, AU, CA and more
- **Limit**: 250 calls/month free

### 2. Jooble API
- **URL**: https://jooble.org/api/about
- **Cost**: Free
- **Coverage**: Global
- **Limit**: Contact for limits

### 3. The Muse API
- **URL**: https://www.themuse.com/developers/api/v2
- **Cost**: Free
- **Coverage**: US focused
- **Limit**: No official limit

### 4. GitHub Jobs API (Deprecated)
- **Status**: Shutdown in 2021
- **Alternative**: Use GitHub search for "hiring" issues

### 5. USA Jobs API
- **URL**: https://developer.usajobs.gov/
- **Cost**: Free
- **Coverage**: US Government jobs only
- **Limit**: Generous

## Option 4: RSS Feeds (Free)

Many job sites offer RSS feeds:

```python
import feedparser

# Indeed RSS
feed = feedparser.parse('https://www.indeed.com/rss?q=python+developer&l=remote')

# SimplyHired RSS
feed = feedparser.parse('https://www.simplyhired.com/search?q=python+developer&l=remote&format=rss')
```

**Limitations**:
- Limited data
- No advanced filtering
- May not include all jobs

## Option 5: Web Scraping (Not Recommended)

If you must scrape, use these ethical practices:

### Requirements
```python
pip install selenium beautifulsoup4 undetected-chromedriver
```

### Ethical Scraping Rules
1. ✅ Respect robots.txt
2. ✅ Add delays between requests
3. ✅ Use realistic user agents
4. ✅ Limit request rate
5. ✅ Cache results
6. ❌ Don't scrape if ToS prohibits it

### Example (Educational Only)
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

# Add delays to be respectful
time.sleep(2)

# Indeed example (check ToS first!)
driver.get("https://www.indeed.com/jobs?q=python+developer&l=remote")
time.sleep(3)

jobs = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

for job in jobs:
    title = job.find_element(By.CLASS_NAME, "jobTitle").text
    company = job.find_element(By.CLASS_NAME, "companyName").text
    print(f"{title} at {company}")

driver.quit()
```

**Warning**: This violates most sites' ToS and can result in IP bans.

## Recommended Setup by Budget

### Free Budget
1. **SerpAPI free tier** (100 searches/month)
2. **Adzuna API** (250 calls/month)
3. **Jooble API** (unlimited?)
4. **RSS Feeds** (unlimited)

### Small Budget ($10-50/month)
1. **SerpAPI** ($50/month for 5,000 searches)
2. Best ROI and reliability

### No API Budget (100% Free)
1. **RSS Feeds only**
2. **Public job boards with RSS**
3. **Manual job board searches**

## Modified Scraper for SerpAPI

Here's how to modify the project to use SerpAPI instead:

```python
# src/scrapers/serpapi_scraper.py
import os
import requests
from typing import List, Dict, Any, Optional
from .base_scraper import BaseScraper

class SerpApiScraper(BaseScraper):
    """Scraper using SerpAPI for Google Jobs."""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)
        self.api_key = api_key or os.getenv("SERPAPI_KEY")
        self.api_endpoint = "https://serpapi.com/search"

    def search_jobs(self, keywords: str, location: str = "", **kwargs) -> List[Dict[str, Any]]:
        params = {
            "api_key": self.api_key,
            "engine": "google_jobs",
            "q": keywords,
            "location": location or "United States",
            "hl": "en",
            "gl": "us"
        }

        response = requests.get(self.api_endpoint, params=params)
        data = response.json()

        jobs = data.get("jobs_results", [])
        return [self.normalize_job(job) for job in jobs]

    def _extract_external_id(self, raw_job: Dict[str, Any]) -> str:
        return f"serpapi_{raw_job.get('job_id', '')}"

    def _extract_title(self, raw_job: Dict[str, Any]) -> str:
        return raw_job.get("title", "")

    def _extract_company(self, raw_job: Dict[str, Any]) -> str:
        return raw_job.get("company_name", "")

    def _extract_location(self, raw_job: Dict[str, Any]) -> str:
        return raw_job.get("location", "")

    def _extract_description(self, raw_job: Dict[str, Any]) -> str:
        return raw_job.get("description", "")

    def _extract_url(self, raw_job: Dict[str, Any]) -> str:
        return raw_job.get("share_url", raw_job.get("apply_link", ""))
```

## Cost Comparison

| Service | Free Tier | Paid Plans | Best For |
|---------|-----------|------------|----------|
| RapidAPI (multiple) | 100-500/month | $10-100/month | Multi-platform |
| SerpAPI | 100/month | $50/5000 | Best value |
| Adzuna | 250/month | Contact sales | UK/EU jobs |
| Jooble | Unlimited? | Free | Global coverage |
| RSS Feeds | Unlimited | Free | Basic needs |
| Web Scraping | Unlimited | Free (risky) | Not recommended |

## Conclusion

**Recommended approach**:
1. Start with **SerpAPI free tier** (100 searches/month)
2. Add **Jooble API** for additional coverage
3. Use **RSS feeds** as backup
4. Upgrade to paid SerpAPI if you need more

**Avoid**:
- Direct web scraping (legal issues)
- Violating Terms of Service
- Getting your IP banned

Choose based on your needs and budget!
