# API Documentation

Complete API reference for the Job Search AI Agent.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication. For production use, implement API key authentication by setting the `N8N_WEBHOOK_AUTH_TOKEN` environment variable.

## Endpoints

### Health Check

Check if the API server is running.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "job-search-agent"
}
```

---

### Search Jobs

Search for jobs across all configured platforms.

**Endpoint:** `POST /api/search`

**Request Body:**
```json
{
  "keywords": "Python Developer",
  "location": "Remote",
  "analyze": true,
  "save_to_db": true,
  "page": "1",
  "date_posted": "week",
  "job_type": "fulltime"
}
```

**Parameters:**
- `keywords` (required): Job search keywords
- `location` (optional): Job location (default: "")
- `analyze` (optional): Run AI analysis (default: true)
- `save_to_db` (optional): Save to database (default: true)
- `page` (optional): Page number for pagination
- `date_posted` (optional): Filter by date ("day", "week", "month")
- `job_type` (optional): Job type filter

**Response:**
```json
{
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
  "jobs": [
    {
      "external_id": "indeed_abc123",
      "source": "indeed",
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "location": "Remote",
      "description": "Job description...",
      "url": "https://...",
      "job_type": "full-time",
      "remote_type": "remote",
      "salary_min": 100000,
      "salary_max": 150000,
      "ai_summary": "Looking for experienced Python developer...",
      "ai_extracted_skills": ["Python", "Django", "AWS"],
      "posted_date": "2025-01-01T00:00:00"
    }
  ],
  "timestamp": "2025-01-01T12:00:00"
}
```

---

### Get Jobs

Retrieve jobs from the database.

**Endpoint:** `GET /api/jobs`

**Query Parameters:**
- `limit` (optional): Maximum number of jobs (default: 100)
- `source` (optional): Filter by platform (indeed, linkedin, glassdoor, monster)
- `keywords` (optional): Filter by keywords in title/description

**Example:**
```
GET /api/jobs?limit=50&source=linkedin&keywords=python
```

**Response:**
```json
{
  "count": 50,
  "jobs": [...]
}
```

---

### Get Job by ID

Get a specific job by database ID.

**Endpoint:** `GET /api/jobs/{job_id}`

**Example:**
```
GET /api/jobs/123
```

**Response:**
```json
{
  "id": 123,
  "external_id": "indeed_abc123",
  "title": "Python Developer",
  "company": "Tech Corp",
  ...
}
```

**Error Response (404):**
```json
{
  "error": "Job not found"
}
```

---

### n8n Webhook

Webhook endpoint optimized for n8n integration.

**Endpoint:** `POST /webhook/job-search`

**Request Body:**
```json
{
  "keywords": "Data Scientist",
  "location": "New York",
  "options": {
    "analyze": true,
    "save_to_db": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "Found 75 jobs, saved 20 new jobs",
  "data": {
    "keywords": "Data Scientist",
    "location": "New York",
    "total_jobs": 75,
    "new_jobs_saved": 20,
    "platform_breakdown": {...},
    "jobs": [...],
    "timestamp": "2025-01-01T12:00:00"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message",
  "message": "Search failed"
}
```

---

### Analyze Job

Analyze a job description with AI.

**Endpoint:** `POST /api/analyze`

**Request Body:**
```json
{
  "title": "Software Engineer",
  "description": "We are looking for an experienced software engineer with expertise in Python, Django, and AWS. 5+ years of experience required..."
}
```

**Response:**
```json
{
  "required_skills": ["Python", "Django", "AWS"],
  "preferred_skills": ["Docker", "Kubernetes"],
  "experience_years": 5,
  "education_level": "Bachelor's",
  "remote_friendly": true,
  "key_responsibilities": [
    "Develop backend services",
    "Design scalable systems"
  ],
  "technologies": ["Python", "Django", "AWS", "PostgreSQL"],
  "soft_skills": ["Communication", "Teamwork"],
  "salary_indicators": "$120k-$150k",
  "summary": "Senior role requiring 5+ years Python experience with Django and AWS, building scalable backend systems."
}
```

---

### Get Statistics

Get database statistics.

**Endpoint:** `GET /api/stats`

**Response:**
```json
{
  "total_jobs": 1234,
  "jobs_by_source": {
    "indeed": 400,
    "linkedin": 350,
    "glassdoor": 250,
    "monster": 234
  },
  "recent_searches": 50
}
```

---

## Error Responses

All endpoints may return error responses:

### 400 Bad Request
```json
{
  "error": "Missing required field: keywords"
}
```

### 404 Not Found
```json
{
  "error": "Endpoint not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Error message details"
}
```

---

## Rate Limiting

API rate limiting can be configured in `config/config.yaml`:

```yaml
api:
  rate_limit:
    enabled: true
    calls: 100
    period: 3600  # 1 hour
```

---

## CORS

CORS is enabled for the following origins (configurable):
- `http://localhost:5678` (n8n default)
- `http://localhost:3000`

Configure in `config/config.yaml`:

```yaml
api:
  cors_origins:
    - "http://localhost:5678"
    - "http://your-n8n-instance.com"
```

---

## Example Usage

### Python

```python
import requests

# Search for jobs
response = requests.post(
    "http://localhost:5000/api/search",
    json={
        "keywords": "Python Developer",
        "location": "Remote",
        "analyze": True
    }
)

data = response.json()
print(f"Found {data['total_jobs']} jobs")

# Get jobs from database
response = requests.get(
    "http://localhost:5000/api/jobs",
    params={"limit": 10, "source": "linkedin"}
)

jobs = response.json()["jobs"]
for job in jobs:
    print(f"{job['title']} at {job['company']}")
```

### JavaScript

```javascript
// Search for jobs
const response = await fetch('http://localhost:5000/api/search', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    keywords: 'Frontend Developer',
    location: 'San Francisco',
    analyze: true
  })
});

const data = await response.json();
console.log(`Found ${data.total_jobs} jobs`);
```

### cURL

```bash
# Search for jobs
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "DevOps Engineer",
    "location": "Remote",
    "analyze": true
  }'

# Get jobs
curl "http://localhost:5000/api/jobs?limit=20&source=indeed"

# Get statistics
curl http://localhost:5000/api/stats
```

---

## Deployment

For production deployment:

1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up reverse proxy (Nginx, Apache)
3. Enable HTTPS
4. Implement authentication
5. Configure rate limiting
6. Set up monitoring and logging

Example with Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 src.api.server:app
```
