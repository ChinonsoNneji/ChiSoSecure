from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "ChiSoSecure"
    assert data["status"] == "operational"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


def test_events_endpoint_available():
    response = client.get("/events")

    assert response.status_code == 200


def test_alerts_endpoint_available():
    response = client.get("/alerts")

    assert response.status_code == 200


def test_incidents_endpoint_available():
    response = client.get("/incidents")

    assert response.status_code == 200


def test_response_actions_endpoint_available():
    response = client.get(
        "/response-actions"
    )

    assert response.status_code == 200