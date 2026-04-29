from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

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
