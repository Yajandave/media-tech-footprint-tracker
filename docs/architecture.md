# Architecture

## System overview

The project has three main layers:

1. React/Vite frontend dashboard
2. FastAPI backend API
3. SQLite database accessed through SQLAlchemy

It is designed as a portfolio demo of an internal analytics platform. The system uses synthetic data only.

## Data flow

```text
Synthetic seed data
        |
        v
SQLite database
        |
        v
FastAPI REST API
        |
        v
React dashboard
        |
        v
Metric cards, filters, charts and tables
```

## Main entities

- `Technology`: media technologies such as Spatial Audio and HDR Video.
- `Product`: synthetic products with platform, region and business unit fields.
- `Integration`: simulated upstream data sources and health status.
- `UsageEvent`: dated usage records linking technologies, products and integrations.

## Backend design

The FastAPI backend exposes:

- Health check endpoint.
- Reference data endpoints for technologies and products.
- Usage event endpoint with a limit parameter.
- Analytics endpoints for summary metrics, adoption, regional usage, integration health and usage trends.

The analytics endpoints use SQL aggregation through SQLAlchemy. Summary, adoption, regional usage and usage trends support optional filters for:

- `region`
- `platform`
- `technology`

SQLite is used to keep setup simple for local development and portfolio review. The database URL can be overridden with `DATABASE_URL`, but the default demo path remains the local SQLite file.

## Frontend design

The React dashboard uses the backend API to display:

- Summary metric cards.
- Region, platform and technology filters.
- Technology adoption chart.
- Playback-hours chart.
- Usage trend chart.
- Regional usage table.
- Integration health table.

The frontend is intentionally simple: it uses React state, `fetch`, and Recharts rather than adding state-management or data-fetching libraries.

The API base URL defaults to `http://127.0.0.1:8000` for local development and can be configured with `VITE_API_BASE_URL` for deployment.

## Deployment readiness

The app is prepared for a simple split deployment:

```text
Static frontend host -> deployed FastAPI backend -> SQLite demo database
```

Deployment-specific configuration is environment-driven:

- `VITE_API_BASE_URL`: frontend setting for the backend API URL.
- `ALLOWED_ORIGINS`: backend CORS allow-list for deployed frontend origins.
- `DATABASE_URL`: optional backend database URL override.

This keeps local setup unchanged while allowing hosted frontend and backend URLs to be connected later. See `docs/deployment.md` for the deployment checklist.

## Continuous integration

The repository has two GitHub Actions workflows:

- Backend workflow: installs Python dependencies, seeds the SQLite database and runs Pytest.
- Frontend workflow: installs Node dependencies and runs the Vite production build.

These workflows give the project basic confidence checks before a deployment branch is merged.

## Why this design

The design mirrors a small internal analytics platform where product, engineering or business users need visibility into adoption trends and data integration health. The implementation prioritizes readability, local setup and recruiter review over production-scale infrastructure.

## Current limitations

- Synthetic data only.
- SQLite local database rather than a hosted production database.
- Hosted SQLite demos may reset when a platform rebuilds or restarts the backend service.
- No authentication or user roles yet.
- Deployment configuration is prepared, but no hosted environment is included in the repository yet.
- No frontend unit or end-to-end tests yet.
