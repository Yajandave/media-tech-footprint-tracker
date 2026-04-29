# Architecture

## System overview

The project has three main layers:

1. React/Vite frontend dashboard
2. FastAPI backend API
3. SQLite database accessed through SQLAlchemy

It is designed as a local portfolio demo of an internal analytics platform. The system uses synthetic data only.

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

SQLite is used to keep setup simple for local development and portfolio review.

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

## Continuous integration

The repository has two GitHub Actions workflows:

- Backend workflow: installs Python dependencies, seeds the SQLite database and runs Pytest.
- Frontend workflow: installs Node dependencies and runs the Vite production build.

These workflows give the project basic confidence checks without adding deployment complexity.

## Why this design

The design mirrors a small internal analytics platform where product, engineering or business users need visibility into adoption trends and data integration health. The implementation prioritizes readability, local setup and recruiter review over production-scale infrastructure.

## Current limitations

- Synthetic data only.
- SQLite local database rather than a hosted production database.
- No authentication or user roles yet.
- No deployment configuration yet.
- No frontend unit or end-to-end tests yet.
