# Deployment Preparation

This project is prepared for a simple split deployment:

```text
React/Vite frontend -> static hosting
FastAPI backend     -> Python web service hosting
SQLite database     -> local demo database seeded from synthetic data
```

The repository does not deploy anything automatically. These notes describe the environment variables and platform settings needed for a portfolio demo deployment.

## Recommended demo architecture

For a beginner-friendly portfolio deployment, use separate services:

- Frontend: Vercel, Netlify or another static site host.
- Backend: Render, Railway, Fly.io or another Python web service host.
- Database: the existing SQLite demo database for synthetic data only.

SQLite keeps the demo simple, but it is not a production database choice for shared multi-user hosting. A production version would use a managed database and migrations.

## Backend configuration

The backend keeps local defaults, but can be configured with environment variables.

```text
ALLOWED_ORIGINS=https://your-frontend-url.example
DATABASE_URL=sqlite:///./media_tech_tracker.db
```

`ALLOWED_ORIGINS` is a comma-separated allow-list for browser origins that can call the API. Set it to the deployed frontend URL after the frontend is live.

`DATABASE_URL` is optional. The app defaults to the local SQLite database path. External databases would require adding the correct database driver dependency and migration strategy.

Suggested Python web service settings:

```text
Root directory: backend
Install command: pip install -r requirements.txt
Seed command: python -m app.seed_data
Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Some hosts do not have a dedicated seed command. In that case, run `python -m app.seed_data` manually from the host shell or as a one-time job before opening the dashboard.

Smoke-test the deployed backend:

```text
GET https://your-backend-url.example/health
GET https://your-backend-url.example/analytics/usage-trends
```

## Frontend configuration

The frontend reads the backend API URL from Vite environment variables.

```text
VITE_API_BASE_URL=https://your-backend-url.example
```

Suggested static host settings:

```text
Root directory: frontend
Install command: npm install
Build command: npm run build
Output directory: dist
```

After the frontend is deployed, copy its final URL into the backend `ALLOWED_ORIGINS` value.

## Local environment files

Use the example files as templates:

```text
backend/.env.example
frontend/.env.example
```

Do not commit real `.env` files. The repository ignores `.env` and `.env.*` files while keeping `.env.example` files tracked.

## Deployment checklist

1. Deploy the backend service.
2. Seed the backend database with synthetic data.
3. Confirm `/health` returns `{ "status": "ok" }`.
4. Deploy the frontend with `VITE_API_BASE_URL` set to the backend URL.
5. Update backend `ALLOWED_ORIGINS` with the frontend URL.
6. Open the dashboard and confirm metric cards, filters, tables and the usage trend chart load.
7. Re-run GitHub Actions or local checks before linking the deployment in the README.

## Known deployment limitations

- The app uses synthetic seed data only.
- The default SQLite database may reset when a hosting platform rebuilds or restarts the service.
- There is no authentication yet, so hosted demos should only expose synthetic data.
- The backend and frontend are deployed as separate services rather than one unified production stack.
