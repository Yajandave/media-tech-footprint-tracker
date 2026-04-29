# Architecture

## System overview

The project has three layers:

1. React frontend
2. FastAPI backend
3. SQLite database

## Data flow

```text
Synthetic seed data
        ↓
SQLite database
        ↓
FastAPI REST API
        ↓
React dashboard
        ↓
Charts, metrics and tables
```

## Main entities

- Technology
- Product
- UsageEvent
- Integration

## Why this design

The design mirrors an internal usage analytics platform where technology adoption and integration health need to be visible to product, engineering and business teams.
