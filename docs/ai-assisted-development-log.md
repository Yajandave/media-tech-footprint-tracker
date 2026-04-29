# AI-Assisted Development Log

Use this document to record how AI helped during the project.

## Requirements breakdown

Prompt used:

> Convert this internship description into technical project requirements for a portfolio project.

Result:

- Internal data platform
- Usage tracking
- Database schema
- REST API
- Dashboard
- Testing
- Documentation

## Database design

AI suggested multiple schema options. The final MVP schema was simplified to:

- technologies
- products
- integrations
- usage_events

## Code generation

AI was used to draft starter code for:

- FastAPI route structure
- SQLAlchemy models
- React dashboard layout
- README documentation

## Manual review

All AI-generated code was reviewed manually.

Checks performed:

- Does the API run locally?
- Do endpoints return valid JSON?
- Are table relationships clear?
- Are field names understandable?
- Does the frontend fail gracefully if the backend is down?

## Testing

AI helped suggest Pytest test cases.

Manually validated:

- Health endpoint
- Analytics summary endpoint
- Dashboard loading
- API response shape

## Reflection

The goal was not to let AI build the project blindly. The goal was to use AI as an engineering assistant while still controlling design decisions, implementation quality and testing.
