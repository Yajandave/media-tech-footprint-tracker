# Media Technology Footprint Tracker

A full-stack portfolio project that simulates an internal analytics platform for tracking usage of media technologies across products, regions, platforms, and teams.

This is designed as a Dolby-inspired internship portfolio project using synthetic data only.

## What it demonstrates

- FastAPI backend
- SQL database design
- REST API development
- Synthetic usage data generation
- Analytics endpoints
- React dashboard
- AI-assisted development documentation
- Testing with Pytest
- GitHub Actions CI workflow

## Project idea

A media technology company needs to understand where its technologies are used, how adoption changes over time, and whether data integrations are healthy.

This platform tracks synthetic technologies such as:

- Spatial Audio
- HDR Video
- Voice Enhancement
- Noise Reduction
- Gaming Audio
- Cinema Audio

## Local setup

### 1. Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
python -m app.seed_data
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

### 2. Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Then open the local Vite URL shown in the terminal.

## Main API endpoints

```text
GET /health
GET /technologies
GET /products
GET /usage-events
GET /analytics/summary
GET /analytics/technology-adoption
GET /analytics/regional-usage
GET /analytics/integration-health
```

## Portfolio positioning

CV bullet:

> Built a full-stack Media Technology Footprint Tracker using FastAPI, React and SQL, simulating an internal data platform for tracking technology adoption, regional usage, integration health and product footprint across synthetic media technology data.

Interview explanation:

> I treated the project as an internal data platform problem. I designed the database, generated synthetic usage data, created REST APIs, built a React dashboard, added analytics endpoints, wrote tests, and documented how I used AI responsibly during development.
