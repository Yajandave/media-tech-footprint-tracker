from fastapi.testclient import TestClient

from app.main import app
from app.seed_data import create_seed_data, reset_database

client = TestClient(app)


def setup_module():
    reset_database()
    create_seed_data()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_technologies_endpoint_returns_seeded_technologies():
    response = client.get("/technologies")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 6
    assert {"id", "name", "category", "description"}.issubset(data[0].keys())


def test_products_endpoint_returns_seeded_products():
    response = client.get("/products")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 24
    assert {"id", "product_name", "platform", "region", "business_unit"}.issubset(
        data[0].keys()
    )


def test_usage_events_endpoint_returns_limited_recent_events():
    response = client.get("/usage-events", params={"limit": 5})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 5
    assert {"date", "active_users", "playback_hours", "api_calls", "error_rate"}.issubset(
        data[0].keys()
    )


def test_summary_endpoint_returns_expected_keys():
    response = client.get("/analytics/summary")
    assert response.status_code == 200

    data = response.json()
    expected_keys = [
        "total_technologies",
        "total_products",
        "total_usage_events",
        "total_active_users",
        "total_playback_hours",
        "average_error_rate",
        "highest_adoption_technology",
        "top_region",
    ]

    for key in expected_keys:
        assert key in data

    assert data["total_usage_events"] == 1440
    assert data["total_active_users"] > 0


def test_technology_adoption_endpoint_returns_ranked_metrics():
    response = client.get("/analytics/technology-adoption")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 6
    assert {"technology", "category", "active_users", "playback_hours", "average_error_rate"}.issubset(
        data[0].keys()
    )
    assert data[0]["active_users"] >= data[-1]["active_users"]


def test_regional_usage_endpoint_returns_region_platform_metrics():
    response = client.get("/analytics/regional-usage")
    assert response.status_code == 200

    data = response.json()
    assert len(data) > 0
    assert {"region", "platform", "active_users", "playback_hours"}.issubset(
        data[0].keys()
    )


def test_integration_health_endpoint_returns_source_metrics():
    response = client.get("/analytics/integration-health")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 4
    assert {
        "source_name",
        "source_type",
        "status",
        "last_sync",
        "events_received",
        "average_error_rate",
    }.issubset(data[0].keys())


def test_usage_trends_endpoint_returns_date_ordered_metrics():
    response = client.get("/analytics/usage-trends")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 120
    assert {"date", "active_users", "playback_hours", "api_calls"}.issubset(
        data[0].keys()
    )
    assert data[0]["date"] == "2026-01-01"
    assert data[-1]["date"] == "2026-04-30"
    assert [row["date"] for row in data] == sorted(row["date"] for row in data)


def test_filtered_usage_trends_endpoint_matches_filtered_summary():
    params = {"technology": "Spatial Audio", "region": "Europe"}

    trends_response = client.get("/analytics/usage-trends", params=params)
    summary_response = client.get("/analytics/summary", params=params)
    adoption_response = client.get("/analytics/technology-adoption", params=params)
    regional_response = client.get("/analytics/regional-usage", params=params)

    assert trends_response.status_code == 200
    assert summary_response.status_code == 200
    assert adoption_response.status_code == 200
    assert regional_response.status_code == 200

    trends = trends_response.json()
    summary = summary_response.json()
    adoption = adoption_response.json()
    regional = regional_response.json()

    assert len(trends) > 0
    assert sum(row["active_users"] for row in trends) == summary["total_active_users"]
    assert sum(row["api_calls"] for row in trends) > 0
    assert {row["technology"] for row in adoption} == {"Spatial Audio"}
    assert {row["region"] for row in regional} == {"Europe"}
