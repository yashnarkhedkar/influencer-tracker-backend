# Influencer Tracker Backend

Backend API for managing influencer marketing campaigns, influencers, and dashboard insights. Built with Django + Django REST Framework.

## Features
- CRUD APIs for campaigns, influencers, and campaign-influencer relationships
- Dashboard analytics endpoints (summary, status breakdown, budgets, trends, platform mix)
- AI tools for campaign briefs and title/hashtag suggestions (OpenAI)
- YouTube channel stats refresh (YouTube Data API v3)

## Tech Stack
- Python 3, Django 4.2, Django REST Framework
- PostgreSQL or SQLite (via `DATABASE_URL`)
- OpenAI API and Google API client

## Project Structure
- `config/`: Django project config
- `campaigns/`: Campaign and influencer models + APIs
- `dashboard/`: Analytics endpoints and AI insights
- `ai_tools/`: OpenAI-powered helper endpoints
- `core/`: Shared utilities (pagination)

## Setup

### 1) Create and activate a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Configure environment variables
Create a `.env` file in the project root:
```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000
YOUTUBE_API_KEY=your-youtube-api-key
OPENAI_API_KEY=your-openai-api-key
```

Notes:
- `DATABASE_URL` defaults to `sqlite:///db.sqlite3` if not set.
- `YOUTUBE_API_KEY` is required for influencer `refresh_stats`.
- `OPENAI_API_KEY` is required for AI endpoints and AI insights.

### 4) Run migrations
```bash
python manage.py migrate
```

### 5) Start the server
```bash
python manage.py runserver
```

Server will be available at `http://127.0.0.1:8000`.

## API Endpoints
Base path: `/api/v1/`

### Campaigns
- `GET /campaigns/`
- `POST /campaigns/`
- `GET /campaigns/{id}/`
- `PATCH /campaigns/{id}/`
- `DELETE /campaigns/{id}/`

Query params:
- `status` (e.g., `active`, `paused`, `completed`)
- `platform` (e.g., `youtube`, `instagram`, `tiktok`)

### Influencers
- `GET /influencers/`
- `POST /influencers/`
- `GET /influencers/{id}/`
- `PATCH /influencers/{id}/`
- `DELETE /influencers/{id}/`
- `POST /influencers/{id}/refresh_stats/` (fetches YouTube stats)

### Campaign Influencers
- `GET /campaign-influencers/`
- `POST /campaign-influencers/`
- `GET /campaign-influencers/{id}/`
- `PATCH /campaign-influencers/{id}/`
- `DELETE /campaign-influencers/{id}/`

Query params:
- `campaign` (campaign UUID)

### Dashboard
- `GET /dashboard/summary/`
- `GET /dashboard/campaigns-by-status/`
- `GET /dashboard/budget-overview/`
- `GET /dashboard/campaigns-over-time/`
- `GET /dashboard/platform-breakdown/`
- `GET /dashboard/ai-insights/`

Note: `ai-insights` currently returns a placeholder value (`"Dummy Insights"`) before calling OpenAI. See `dashboard/ai.py`.

### AI Tools
- `POST /ai/generate-brief/`
  - Body: `product_name`, `target_audience`, `platform`, `tone`, `budget`
- `POST /ai/suggest-titles-hashtags/`
  - Body: `description`, `platform`

## Production
A sample `Procfile` is included for Gunicorn:
```bash
web: gunicorn config.wsgi --log-file -
```

## License
Specify your license here.
