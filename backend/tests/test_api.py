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


def test_protected_events_endpoint_requires_auth():
    response = client.get("/events")

    assert response.status_code == 401


def test_protected_alerts_endpoint_requires_auth():
    response = client.get("/alerts")

    assert response.status_code == 401


def test_protected_incidents_endpoint_requires_auth():
    response = client.get("/incidents")

    assert response.status_code == 401


def test_protected_response_actions_requires_auth():
    response = client.get("/response-actions")

    assert response.status_code == 401


def test_protected_users_endpoint_requires_auth():
    response = client.get("/users")

    assert response.status_code == 401