import uuid
from collections.abc import Iterator
from typing import Any

import pytest
from fakes import FakeIncidentRepository, FakeTransaction
from fastapi.testclient import TestClient

from plantassist.api.deps import get_incident_service
from plantassist.config import Settings, get_settings
from plantassist.main import create_app
from plantassist.services.incidents import IncidentService

pytestmark = pytest.mark.unit

BASE = "/api/v1/incidents"


@pytest.fixture
def api(settings: Settings) -> Iterator[TestClient]:
    """
    A client whose incident service runs on in-memory fakes.
    """
    service = IncidentService(FakeIncidentRepository(), FakeTransaction())
    app = create_app(settings)
    app.dependency_overrides[get_settings] = lambda: settings
    app.dependency_overrides[get_incident_service] = lambda: service
    with TestClient(app) as client:
        yield client


def create(api: TestClient, **overrides: Any) -> dict[str, Any]:
    payload = {
        "machineId": "CP-01",
        "alarmCode": "SERVO-7021",
        "title": "Servo axis 4 following error",
        "symptoms": "Fault during rapid acceleration",
    } | overrides
    response = api.post(BASE, json=payload)
    assert response.status_code == 201, response.text
    body: dict[str, Any] = response.json()
    return body


def test_create_returns_201_with_camel_case_body(api: TestClient) -> None:
    body = create(api)

    assert body["status"] == "OPEN"
    assert body["machineId"] == "CP-01"
    uuid.UUID(body["id"])  # raises if the ID isn't a valid UUID


def test_create_rejects_invalid_body(api: TestClient) -> None:
    response = api.post(BASE, json={"machineId": "CP-01", "title": "   ", "symptoms": "x"})

    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "VALIDATION_ERROR"
    assert any(detail["field"] == "body.title" for detail in body["details"])


def test_get_returns_created_incident(api: TestClient) -> None:
    created = create(api)

    response = api.get(f"{BASE}/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_unknown_incident_returns_404(api: TestClient) -> None:
    response = api.get(f"{BASE}/{uuid.uuid4()}")

    assert response.status_code == 404
    assert response.json()["code"] == "INCIDENT_NOT_FOUND"


def test_get_malformed_id_returns_422(api: TestClient) -> None:
    response = api.get(f"{BASE}/not-a-uuid")

    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_list_filters_and_pages(api: TestClient) -> None:
    create(api, machineId="CP-01")
    create(api, machineId="CP-01")
    create(api, machineId="CV-02")

    response = api.get(BASE, params={"machineId": "CP-01", "page": 1, "size": 1})

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert len(body["items"]) == 1
    assert (body["page"], body["size"]) == (1, 1)


@pytest.mark.parametrize("params", [{"page": 0}, {"size": 0}, {"size": 101}, {"status": "BROKEN"}])
def test_list_rejects_invalid_query(api: TestClient, params: dict[str, Any]) -> None:
    response = api.get(BASE, params=params)

    assert response.status_code == 422
    assert response.json()["code"] == "VALIDATION_ERROR"


def test_record_resolution_resolves_incident(api: TestClient) -> None:
    created = create(api)

    response = api.patch(
        f"{BASE}/{created['id']}/resolution",
        json={"resolution": "Encoder connector was loose."},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "RESOLVED"
    assert response.json()["resolvedAt"] is not None


def test_resolving_twice_returns_409(api: TestClient) -> None:
    created = create(api)
    url = f"{BASE}/{created['id']}/resolution"
    api.patch(url, json={"resolution": "First fix"})

    response = api.patch(url, json={"resolution": "Second fix"})

    assert response.status_code == 409
    assert response.json()["code"] == "INVALID_STATUS_TRANSITION"


def test_resolving_unknown_incident_returns_404(api: TestClient) -> None:
    response = api.patch(f"{BASE}/{uuid.uuid4()}/resolution", json={"resolution": "x"})

    assert response.status_code == 404
    assert response.json()["code"] == "INCIDENT_NOT_FOUND"
