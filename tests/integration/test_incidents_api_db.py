from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from pydantic import PostgresDsn

from plantassist.config import Settings, get_settings
from plantassist.main import create_app

pytestmark = pytest.mark.integration

BASE = "/api/v1/incidents"


@pytest.fixture
def db_api(database_url: str) -> Iterator[TestClient]:
    """
    The real app, wired to the test database. No fakes.
    """
    settings = Settings(_env_file=None, app_env="ci", database_url=PostgresDsn(database_url))
    app = create_app(settings)
    app.dependency_overrides[get_settings] = lambda: settings
    with TestClient(app) as client:
        yield client


def test_incident_lifecycle_through_http(db_api: TestClient) -> None:
    created = db_api.post(
        BASE,
        json={"machineId": "CP-01", "title": "Servo fault", "symptoms": "Following error"},
    )
    assert created.status_code == 201, created.text
    incident_id = created.json()["id"]

    listed = db_api.get(BASE, params={"machineId": "CP-01"})
    assert listed.json()["total"] == 1

    resolved = db_api.patch(
        f"{BASE}/{incident_id}/resolution", json={"resolution": "Encoder connector was loose."}
    )
    assert resolved.status_code == 200
    assert resolved.json()["status"] == "RESOLVED"

    again = db_api.patch(f"{BASE}/{incident_id}/resolution", json={"resolution": "Again"})
    assert again.status_code == 409
    assert again.json()["code"] == "INVALID_STATUS_TRANSITION"

    fetched = db_api.get(f"{BASE}/{incident_id}")
    assert fetched.json()["resolution"] == "Encoder connector was loose."


def test_ready_when_database_is_up(db_api: TestClient) -> None:
    response = db_api.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "checks": {"database": "ok"}}
