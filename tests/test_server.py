from fastapi.testclient import TestClient

from solar_server import server


def test_health_endpoint(monkeypatch):
    monkeypatch.setenv("SOLAR_DATABASE_PATH", ":memory:")
    monkeypatch.setenv("SOLAR_FETCH_INTERVAL_SECONDS", "3600")
    monkeypatch.setenv("SOLAR_SEED_TEST_DATA", "false")
    monkeypatch.setattr(
        server,
        "fetch_reading",
        lambda source_url=None: {
            "timestamp": "2026-05-28T10:00:00Z",
            "plant_id": "hochschule-pv-1",
            "power_w": 500.0,
            "energy_today_kwh": 1.2,
            "temperature_c": 21.5,
        },
    )

    with TestClient(server.app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_dashboard_page_is_served(monkeypatch):
    monkeypatch.setenv("SOLAR_DATABASE_PATH", ":memory:")
    monkeypatch.setenv("SOLAR_FETCH_INTERVAL_SECONDS", "3600")
    monkeypatch.setenv("SOLAR_SEED_TEST_DATA", "false")
    monkeypatch.setattr(
        server,
        "fetch_reading",
        lambda source_url=None: {
            "timestamp": "2026-05-28T10:00:00Z",
            "plant_id": "hochschule-pv-1",
            "power_w": 500.0,
            "energy_today_kwh": 1.2,
            "temperature_c": 21.5,
        },
    )

    with TestClient(server.app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Solarenergie Dashboard" in response.text


def test_summary_endpoint_returns_prepared_values(monkeypatch):
    monkeypatch.setenv("SOLAR_DATABASE_PATH", ":memory:")
    monkeypatch.setenv("SOLAR_FETCH_INTERVAL_SECONDS", "3600")
    monkeypatch.setenv("SOLAR_SEED_TEST_DATA", "false")
    monkeypatch.setattr(
        server,
        "fetch_reading",
        lambda source_url=None: {
            "timestamp": "2026-05-28T10:00:00Z",
            "plant_id": "hochschule-pv-1",
            "power_w": 500.0,
            "energy_today_kwh": 1.2,
            "temperature_c": 21.5,
        },
    )

    with TestClient(server.app) as client:
        response = client.get("/summary")

    assert response.status_code == 200
    assert response.json()["average_power_w"] == 500.0
