from importlib.metadata import version

import pytest
from fastapi.testclient import TestClient

pytestmark = pytest.mark.unit

def test_live_returns_ok(client: TestClient) -> None:
    response = client.get("/health/live")

    assert response.status_code ==  200
    assert response.json() == {"status": "ok"}

def test_version_reports_build_info(client: TestClient) -> None:
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "name": "PlantAssist AI",
        "version": version("plantassist"),
        "environment": "ci"
    }

def test_unknown_route_returns_404(client: TestClient) -> None:
    response = client.get("/does-not-exist")

    assert response.status_code == 404

