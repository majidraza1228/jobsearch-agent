# n8n Integration Guide

This guide explains how to integrate the Job Search AI Agent with n8n workflows.

## Overview

The Job Search Agent provides a REST API and webhook endpoints that can be easily integrated into n8n workflows for automated job searching and processing.

## Prerequisites

1. n8n installed and running (local or cloud)
2. Job Search Agent API server running
3. API keys configured (RapidAPI, OpenAI)

## Setup Steps

### 1. Start the Job Search Agent API Server

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Initialize database
python src/database/init_db.py

# Start the API server
python src/api/server.py
```

The server will start on `http://localhost:5000` by default.

### 2. Import the n8n Workflow

1. Open n8n in your browser
2. Click "Add workflow" → "Import from File"
3. Select `n8n-workflows/job-search-workflow.json`
4. The workflow will be imported with all nodes configured

### 3. Configure the Workflow

#### Update API Endpoint URL

In the "Call Job Search Agent" HTTP Request node:
- Update the URL if your API server is running on a different host/port
- Default: `http://localhost:5000/webhook/job-search`

#### Set Search Parameters

The webhook accepts the following JSON payload:

```json
{
  "keywords": "Python Developer",
  "location": "Remote",
  "options": {
    "analyze": true,
    "save_to_db": true
  }
}
```

## Workflow Nodes Explained

### 1. Webhook Trigger
- Triggers the workflow when called via HTTP POST
- Path: `/webhook/job-search`
- Accepts search parameters in request body

### 2. Call Job Search Agent
- Makes HTTP POST request to the agent API
- Sends search parameters
- Receives job search results

### 3. Check Success
- Validates the API response
- Routes to success or error handling

### 4. Process Jobs
- Processes the returned job data
- Can be customized for filtering, transformation

### 5. Respond to Webhook
- Sends response back to webhook caller
- Returns search results

## Usage Examples

### Example 1: Webhook Trigger

Trigger the workflow via HTTP POST:

```bash
curl -X POST http://localhost:5678/webhook/job-search \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Software Engineer",
    "location": "San Francisco",
    "options": {
      "analyze": true,
      "save_to_db": true
    }
  }'
```

### Example 2: Scheduled Search

Enable the "Schedule" node to run automated searches:

1. Enable the "Schedule (Optional)" node
2. Enable the "Set Search Parameters" node
3. Configure the cron expression (default: 9 AM daily)
4. Set your default search parameters

### Example 3: Email Notifications

Enable email notifications for new jobs:

1. Enable the "Send Email Notification" node
2. Configure your email settings:
   - From email
   - To email
   - SMTP credentials (in n8n settings)
3. Customize the email template

## Advanced Integrations

### Slack Notifications

Add a Slack node to send job alerts:

```
Process Jobs → Slack Node
```

Configure the Slack node:
- Channel: #job-alerts
- Message: Job details from `$json.data.jobs`

### Airtable/Google Sheets Storage

Store jobs in a spreadsheet:

```
Process Jobs → Airtable/Google Sheets Node
```

Map fields:
- Title → Job Title
- Company → Company Name
- URL → Job URL
- etc.

### Filter and Match

Add a Code node to filter jobs:

```javascript
// Filter for remote jobs only
const remoteJobs = items[0].json.data.jobs.filter(
  job => job.remote_type === 'remote'
);

return [{ json: { jobs: remoteJobs } }];
```

### Multi-Step Workflows

Create complex workflows:

1. Search for jobs
2. Analyze with AI
3. Match against user profile
4. Filter by match score
5. Send personalized applications
6. Track in CRM

## API Endpoints Reference

### POST /webhook/job-search

Webhook endpoint for n8n integration.

**Request:**
```json
{
  "keywords": "string",
  "location": "string",
  "options": {
    "analyze": boolean,
    "save_to_db": boolean
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Found 150 jobs, saved 45 new jobs",
  "data": {
    "keywords": "Python Developer",
    "location": "Remote",
    "total_jobs": 150,
    "new_jobs_saved": 45,
    "platform_breakdown": {
      "indeed": 50,
      "linkedin": 45,
      "glassdoor": 30,
      "monster": 25
    },
    "jobs": [...]
  }
}
```

### POST /api/search

Alternative search endpoint.

### GET /api/jobs

Retrieve stored jobs from database.

**Query Parameters:**
- `limit`: Number of jobs to return (default: 100)
- `source`: Filter by platform (indeed, linkedin, etc.)
- `keywords`: Filter by keywords

### GET /api/stats

Get database statistics.

## Troubleshooting

### Workflow not triggering
- Check that the API server is running
- Verify the webhook URL is correct
- Check n8n logs for errors

### No jobs returned
- Verify API keys are set correctly
- Check rate limits on RapidAPI
- Review API server logs

### Database errors
- Ensure database is initialized
- Check file permissions for SQLite

## Best Practices

1. **Rate Limiting**: Be mindful of API rate limits
2. **Scheduling**: Don't run searches too frequently
3. **Monitoring**: Set up error notifications
4. **Data Management**: Periodically clean old jobs
5. **Security**: Use environment variables for secrets

## Example Workflows

### Daily Job Digest

1. Schedule trigger (daily at 9 AM)
2. Search multiple job titles
3. Aggregate results
4. Send email digest
5. Save to database

### Job Application Tracker

1. Search for jobs
2. Filter by criteria
3. Store in Airtable
4. Track application status
5. Send follow-up reminders

### Career Dashboard

1. Scheduled searches for target roles
2. AI analysis and scoring
3. Update Google Sheets dashboard
4. Slack notifications for high matches
5. Generate weekly reports

## Support

For issues or questions:
- Check the main README.md
- Review API documentation
- Check n8n community forums
