# RapidAPI Setup Guide

Complete guide to setting up RapidAPI for the Job Search Agent.

## Step 1: Create RapidAPI Account

1. Go to [RapidAPI](https://rapidapi.com/)
2. Click "Sign Up" (top right)
3. Sign up with Google, GitHub, or email
4. Verify your email

## Step 2: Subscribe to Job Search APIs

You need to subscribe to APIs for each job platform you want to search.

### Indeed API

1. Visit: https://rapidapi.com/search/indeed%20jobs
2. Choose an Indeed Jobs API (recommended: "Indeed Jobs Search API")
3. Click "Subscribe to Test"
4. Choose a plan:
   - **Basic (Free)**: 100 requests/month
   - **Pro**: ~$10-30/month for 1000-5000 requests
5. Click "Subscribe"

### LinkedIn Jobs API

1. Visit: https://rapidapi.com/search/linkedin%20jobs
2. Choose a LinkedIn Jobs API (recommended: "LinkedIn Data API")
3. Subscribe to a plan (usually $10-50/month)

### Glassdoor API

1. Visit: https://rapidapi.com/search/glassdoor%20jobs
2. Choose a Glassdoor Jobs API
3. Subscribe to a plan

### Monster API

1. Visit: https://rapidapi.com/search/monster%20jobs
2. Choose a Monster Jobs API
3. Subscribe to a plan

## Step 3: Get Your API Key

1. Go to [RapidAPI Dashboard](https://rapidapi.com/developer/dashboard)
2. Click on any API you subscribed to
3. Look for "X-RapidAPI-Key" in the code snippets
4. Copy your API key (starts with something like `abc123def456...`)

**Important**: You only need ONE RapidAPI key for all APIs!

## Step 4: Configure Your Project

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your RapidAPI key:
   ```env
   RAPIDAPI_KEY=your_actual_rapidapi_key_here
   OPENAI_API_KEY=your_openai_key_here
   ```

3. Make sure `config/config.yaml` has the platforms enabled:
   ```yaml
   scrapers:
     indeed:
       enabled: true
     linkedin:
       enabled: true
     glassdoor:
       enabled: true
     monster:
       enabled: true
   ```

## Step 5: Test Your Setup

Run a test search:

```bash
python -m src.main --search "Software Engineer" --location "Remote" --limit 5
```

You should see jobs from all enabled platforms!

## Cost Optimization Tips

### 1. Start with Free Tiers
- Most APIs offer 100-500 free requests/month
- Test with free tiers before upgrading

### 2. Choose Selective Platforms
You don't need all 4 platforms. Pick the most relevant:
- **US Jobs**: Indeed + LinkedIn
- **UK/Europe**: LinkedIn + Glassdoor
- **Tech Jobs**: LinkedIn + Glassdoor
- **All Industries**: Indeed + Monster

Edit `config/config.yaml` to disable unwanted platforms:
```yaml
scrapers:
  indeed:
    enabled: true
  linkedin:
    enabled: true
  glassdoor:
    enabled: false  # Disabled
  monster:
    enabled: false  # Disabled
```

### 3. Use Caching
The database automatically caches results, so you won't re-fetch the same jobs.

### 4. Limit Results
Reduce `max_results` in config to save API calls:
```yaml
scrapers:
  indeed:
    enabled: true
    max_results: 25  # Instead of 50
```

### 5. Schedule Wisely
- Don't search too frequently
- Run searches 1-2 times per day max
- Use n8n scheduling to control frequency

## Recommended Plans by Usage

### Light Usage (Personal)
- **Searches**: 2-3 per day
- **Total/month**: ~100 searches
- **Cost**: $0 (free tiers)
- **Platforms**: Pick 1-2 platforms

### Medium Usage (Active Job Seeker)
- **Searches**: 5-10 per day
- **Total/month**: ~300 searches
- **Cost**: $10-30/month
- **Platforms**: 2-3 platforms

### Heavy Usage (Recruiter/Agency)
- **Searches**: 20+ per day
- **Total/month**: 600+ searches
- **Cost**: $50-100/month
- **Platforms**: All 4 platforms

## Troubleshooting

### Error: "You are not subscribed to this API"

**Solution**:
1. Go to RapidAPI dashboard
2. Find the specific API (Indeed, LinkedIn, etc.)
3. Click "Subscribe to Test"
4. Choose a plan

### Error: "Rate limit exceeded"

**Solution**:
1. Check your plan limits on RapidAPI
2. Wait until the limit resets (usually monthly)
3. Upgrade your plan
4. Or reduce search frequency

### Error: "Invalid API key"

**Solution**:
1. Check `.env` file has correct key
2. Make sure there are no extra spaces or quotes
3. Regenerate key on RapidAPI if needed

### No Results Returned

**Solution**:
1. Check API is enabled in `config/config.yaml`
2. Verify API subscription is active
3. Try different search keywords
4. Check API status on RapidAPI

## API Endpoint Reference

The project uses these RapidAPI endpoints by default:

```yaml
indeed:
  api_endpoint: "https://indeed12.p.rapidapi.com/jobs/search"

linkedin:
  api_endpoint: "https://linkedin-data-api.p.rapidapi.com/search-jobs"

glassdoor:
  api_endpoint: "https://glassdoor-job-search.p.rapidapi.com/api/v1/jobs"

monster:
  api_endpoint: "https://monster-job-search.p.rapidapi.com/search"
```

**Note**: Specific API endpoints may vary based on which API you subscribed to. Update `config/config.yaml` if needed.

## Alternative: Mix Free and Paid

You can combine free and paid sources! For example:

```yaml
scrapers:
  # FREE
  serpapi:
    enabled: true  # 100 searches/month free

  # PAID
  linkedin:
    enabled: true  # Most important paid source

  # DISABLED
  indeed:
    enabled: false
  glassdoor:
    enabled: false
  monster:
    enabled: false
```

This gives you:
- 100 free searches from SerpAPI (all platforms)
- Better LinkedIn data from paid API
- Total cost: ~$10-20/month

## Next Steps

1. ✅ Subscribe to APIs on RapidAPI
2. ✅ Add API key to `.env`
3. ✅ Test with a search
4. ✅ Configure n8n integration
5. ✅ Set up scheduled searches

For n8n integration, see [N8N_INTEGRATION.md](N8N_INTEGRATION.md)
