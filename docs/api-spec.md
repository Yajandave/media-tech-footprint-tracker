# API Spec

## GET /health

Returns API health.

## GET /technologies

Returns all tracked technologies.

## GET /products

Returns all products.

## GET /usage-events

Returns recent usage events.

Query parameter:

```text
limit: integer, default 100, max 1000
```

## GET /analytics/summary

Returns high-level platform metrics.

## GET /analytics/technology-adoption

Returns adoption metrics grouped by technology.

## GET /analytics/regional-usage

Returns usage grouped by region and platform.

## GET /analytics/integration-health

Returns health metrics for simulated data integrations.
