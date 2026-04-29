# AI-Assisted Development Log

This document records how AI was used as an engineering assistant while building the Media Technology Footprint Tracker.

The project was not built by accepting AI output blindly. AI was used to speed up planning, generate starter ideas, review gaps and draft implementation options. Design choices, testing decisions and final code review remained manual responsibilities.

## Requirements breakdown

Prompt used:

> Convert this internship description into technical project requirements for a portfolio project.

Resulting project requirements:

- Internal analytics platform concept
- Usage tracking across products, regions and platforms
- Relational database schema
- REST API for reference data and analytics
- Synthetic seed data
- React dashboard
- Testing and CI
- Documentation suitable for portfolio review

## Database design

AI suggested multiple schema options. The final MVP schema was simplified to four main entities:

- `technologies`
- `products`
- `integrations`
- `usage_events`

Manual review focused on whether the schema was understandable, easy to seed and useful for analytics queries.

## Initial implementation

AI helped draft starter code for:

- FastAPI app structure
- SQLAlchemy models
- Synthetic seed data
- API route organization
- React dashboard layout
- README and docs outline

Manual checks included:

- Does the API run locally?
- Do endpoints return valid JSON?
- Are model relationships clear?
- Are field names understandable?
- Does the frontend fail clearly if the backend is not running?

## Milestone 1: backend analytics, tests and API docs

AI was used to help identify missing backend credibility signals and draft the implementation plan.

Changes made:

- Added `GET /analytics/usage-trends`.
- Added analytics filters for `region`, `platform` and `technology`.
- Applied filters to summary, technology adoption, regional usage and usage trends endpoints.
- Expanded Pytest coverage across health, reference data, usage event and analytics endpoints.
- Updated the API spec with query filters and example responses.

Manual review focused on:

- Keeping analytics behavior simple and explainable.
- Avoiding unnecessary backend restructuring.
- Verifying that filtered usage trends matched filtered summary totals.
- Ensuring the API documentation did not overclaim beyond implemented behavior.

Validation:

- Backend GitHub Actions seeded the database successfully.
- Pytest passed for the backend endpoint suite.

## Milestone 2: frontend dashboard improvements

AI was used to help plan dashboard ergonomics and identify the smallest useful frontend changes.

Changes made:

- Added dropdown filters for region, platform and technology.
- Connected filters to the analytics summary, adoption, regional usage and usage trends endpoints.
- Added a usage trend line chart.
- Improved loading, refresh, empty and error states.
- Refined the layout into a cleaner internal analytics dashboard.
- Added a frontend GitHub Actions build workflow.

Manual review focused on:

- Keeping the UI beginner-readable and professional.
- Avoiding unnecessary dependencies.
- Keeping frontend changes separate from backend logic.
- Confirming the dashboard relied on implemented API behavior.

Validation:

- Backend GitHub Actions passed after the frontend changes.
- Frontend GitHub Actions installed dependencies and completed `npm run build` successfully.

## Responsible AI usage

AI was useful for accelerating structure, boilerplate and review checklists. The most important human responsibilities were:

- Choosing a realistic project scope.
- Reviewing generated code for correctness.
- Keeping the project honest about limitations.
- Running CI and addressing failures.
- Writing documentation that accurately describes the implemented system.

## Reflection

The main benefit of AI was reducing the time spent on blank-page drafting and helping surface gaps such as missing CI, tests, filters and API documentation. The project still required manual judgment to keep the implementation small, understandable and portfolio-appropriate.
