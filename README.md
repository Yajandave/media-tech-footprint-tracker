# Media Technology Footprint Tracker

A portfolio-ready full-stack analytics project that simulates an internal platform for tracking media technology adoption across products, regions, platforms and data integrations.

The project uses synthetic data to show how a product or engineering team could monitor where technologies are used, how usage changes over time, and whether upstream data integrations look healthy.

This is an independent portfolio project inspired by media technology internship requirements. It is not affiliated with, endorsed by, or connected to Dolby.

## How this maps to the internship

The project is designed to demonstrate practical skills that are useful for technical internship work on internal data platforms and media technology tooling:

- Translate a business problem into a working software project.
- Model product, technology, usage and integration data in a relational database.
- Build REST API endpoints for operational and analytics use cases.
- Generate realistic synthetic data for a safe public demo.
- Create a dashboard that helps users scan adoption, regional usage, trends and integration health.
- Add automated checks so the backend tests and frontend build run in GitHub Actions.
- Document the system, API and AI-assisted development process clearly enough for review.

## Features

- FastAPI backend with health, reference data, usage event and analytics routes.
- SQLAlchemy models backed by a local SQLite database.
- Synthetic seed data for technologies, products, integrations and usage events.
- Analytics endpoints for summary metrics, technology adoption, regional usage, integration health and usage trends.
- Optional analytics filters for region, platform and technology.
- React/Vite dashboard for metric cards, charts and tables.
- Dashboard filters that update summary cards, adoption chart, regional table and usage trends.
- Usage trend line chart showing active users and playback hours over time.
- Backend GitHub Actions workflow that seeds the database and runs Pytest.
- Frontend GitHub Actions workflow that installs dependencies and runs the production build.
- Deployment-ready environment variables for frontend API URL and backend CORS origins.
- AI-assisted development log explaining how AI was used and manually reviewed.

## Tech stack

```text
Frontend: React, Vite, Recharts
Backend: FastAPI, SQLAlchemy, Pydantic
Database: SQLite
Testing and CI: Pytest, GitHub Actions, npm build
```

## Project structure

```text
backend/        FastAPI app, SQLAlchemy models, seed data and tests
frontend/       React/Vite dashboard
docs/           API spec, architecture, deployment notes, testing plan and AI log
.github/        Backend and frontend GitHub Actions workflows
```

## Local setup

### Backend setup

From the repository root:

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

Install dependencies and seed the local SQLite database:

```bash
pip install -r requirements.txt
python -m app.seed_data
```

Run the backend API:

```bash
uvicorn app.main:app --reload
```

Open the FastAPI docs:

```text
http://127.0.0.1:8000/docs
```

### Frontend setup

Open a second terminal from the repository root:

```bash
cd frontend
npm install
npm run dev
```

Then open the local Vite URL shown in the terminal, usually:

```text
http://localhost:5173
```

The frontend expects the backend to be running at:

```text
http://127.0.0.1:8000
```

For a deployed or non-local backend, set `VITE_API_BASE_URL` in `frontend/.env` or in the hosting provider's environment variables.

## Tests

Run backend tests from the `backend` folder:

```bash
cd backend
pytest
```

The backend GitHub Actions workflow also runs:

```bash
python -m app.seed_data
pytest
```

## Build

Run the frontend production build from the `frontend` folder:

```bash
cd frontend
npm install
npm run build
```

The frontend GitHub Actions workflow runs the same install and build flow.

## Deployment preparation

This repository is prepared for a split demo deployment:

```text
Frontend: static Vite build on Vercel, Netlify or similar
Backend: FastAPI service on Render, Railway, Fly.io or similar
Database: SQLite demo database seeded with synthetic data
```

Deployment-related environment examples are provided in:

```text
backend/.env.example
frontend/.env.example
```

Important environment variables:

```text
VITE_API_BASE_URL=https://your-backend-url.example
ALLOWED_ORIGINS=https://your-frontend-url.example
DATABASE_URL=sqlite:///./media_tech_tracker.db
```

See `docs/deployment.md` for the full deployment checklist, including backend start command, frontend build settings and smoke-test URLs.

No public hosted URL is included yet.

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
GET /analytics/usage-trends
```

Analytics endpoints support these optional query filters where applicable:

```text
region
platform
technology
```

See `docs/api-spec.md` for request examples and response shapes.

## Project limitations

- Uses synthetic data only; it does not contain real partner, customer or product data.
- Independent portfolio project; not affiliated with Dolby.
- SQLite is used for a simple local demo, not production-scale storage.
- A hosted SQLite demo may reset when a platform rebuilds or restarts the backend service.
- No authentication or role-based access control yet.
- The frontend API base URL defaults to local development and must be configured for deployment.
- Data is reseeded manually with `python -m app.seed_data` rather than managed through migrations.
- No public hosted demo URL is documented yet.

## Portfolio positioning

CV bullet:

> Built a full-stack Media Technology Footprint Tracker using FastAPI, React and SQLite, simulating an internal analytics platform for tracking technology adoption, regional usage, integration health and usage trends across synthetic media technology data.

Interview explanation:

> I treated the project as an internal data platform problem. I designed a relational schema, generated synthetic usage data, built FastAPI analytics endpoints, added filters and trend aggregation, created a React dashboard, documented the API and architecture, added GitHub Actions for backend tests and frontend builds, and prepared the app for a simple split deployment.
