# API Spec

Base URL for local development:

```text
http://127.0.0.1:8000
```

## Shared analytics filters

The following optional query filters are available on these endpoints:

- `GET /analytics/summary`
- `GET /analytics/technology-adoption`
- `GET /analytics/regional-usage`
- `GET /analytics/usage-trends`

```text
region: string, optional
platform: string, optional
technology: string, optional
```

Example values from the seed data:

```text
region=Europe
platform=Streaming
technology=Spatial Audio
```

Filters can be combined:

```text
/analytics/usage-trends?region=Europe&technology=Spatial%20Audio
```

## GET /health

Returns API health.

Example response:

```json
{
  "status": "ok"
}
```

## GET /technologies

Returns all tracked technologies.

Example response:

```json
[
  {
    "id": 1,
    "name": "Spatial Audio",
    "category": "Audio",
    "description": "Immersive audio experience"
  }
]
```

## GET /products

Returns all products.

Example response:

```json
[
  {
    "id": 1,
    "product_name": "Product 1",
    "platform": "Streaming",
    "region": "Europe",
    "business_unit": "Consumer Entertainment"
  }
]
```

## GET /usage-events

Returns recent usage events sorted by date descending.

Query parameter:

```text
limit: integer, optional, default 100, minimum 1, maximum 1000
```

Example request:

```text
/usage-events?limit=2
```

Example response:

```json
[
  {
    "id": 1430,
    "technology_id": 1,
    "product_id": 8,
    "integration_id": 2,
    "date": "2026-04-30",
    "active_users": 18450,
    "playback_hours": 51270.75,
    "api_calls": 922500,
    "error_rate": 0.814
  }
]
```

## GET /analytics/summary

Returns high-level platform metrics. Supports the shared analytics filters.

Example request:

```text
/analytics/summary?region=Europe&technology=Spatial%20Audio
```

Example response:

```json
{
  "total_technologies": 1,
  "total_products": 6,
  "total_usage_events": 65,
  "total_active_users": 1180000,
  "total_playback_hours": 2975000.5,
  "average_error_rate": 1.214,
  "highest_adoption_technology": "Spatial Audio",
  "top_region": "Europe"
}
```

## GET /analytics/technology-adoption

Returns adoption metrics grouped by technology. Supports the shared analytics filters.

Example request:

```text
/analytics/technology-adoption?platform=Streaming
```

Example response:

```json
[
  {
    "technology": "Spatial Audio",
    "category": "Audio",
    "active_users": 2450000,
    "playback_hours": 6125000.75,
    "average_error_rate": 1.128
  }
]
```

## GET /analytics/regional-usage

Returns usage grouped by region and platform. Supports the shared analytics filters.

Example request:

```text
/analytics/regional-usage?technology=HDR%20Video
```

Example response:

```json
[
  {
    "region": "Europe",
    "platform": "Streaming",
    "active_users": 875000,
    "playback_hours": 2230000.25
  }
]
```

## GET /analytics/integration-health

Returns health metrics for simulated data integrations.

Example response:

```json
[
  {
    "source_name": "Partner API",
    "source_type": "API",
    "status": "Active",
    "last_sync": "2026-04-29T15:52:47.000000",
    "events_received": 360,
    "average_error_rate": 1.245
  }
]
```

## GET /analytics/usage-trends

Returns usage metrics grouped by date and sorted by date ascending. Supports the shared analytics filters.

Response fields:

```text
date: ISO date string
active_users: integer, summed for the date
playback_hours: number, summed for the date
api_calls: integer, summed for the date
```

Example request:

```text
/analytics/usage-trends?region=Europe&technology=Spatial%20Audio
```

Example response:

```json
[
  {
    "date": "2026-01-01",
    "active_users": 31850,
    "playback_hours": 81536.42,
    "api_calls": 1528800
  },
  {
    "date": "2026-01-02",
    "active_users": 24620,
    "playback_hours": 60319.0,
    "api_calls": 1034040
  }
]
```
