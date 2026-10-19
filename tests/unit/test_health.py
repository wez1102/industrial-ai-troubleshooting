from importlib.metadata import version

import pytest
from fastapi.testclient import TestClient
from pydantic import PostgresDsn

from plantassist.config import Settings, get_settings
from plantassist.main import create_app

pytestmark = pytest.mark.unit


def test_live_returns_ok(client: TestClient) -> None:
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version_reports_build_info(client: TestClient) -> None:
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "name": "PlantAssist AI",
        "version": version("plantassist"),
        "environment": "ci",
        "gitSha": "unknown",
        "buildDate": "unknown",
    }


def test_version_reports_build_information_from_settings() -> None:
    settings = Settings(
        _env_file=None, app_env="ci", git_sha="abc1234", build_date="2026-10-14T18:00:00Z"
    )
    app = create_app(settings)
    app.dependency_overrides[get_settings] = lambda: settings

    with TestClient(app) as client:
        body = client.get("/version").json()

    assert body["gitSha"] == "abc1234"
    assert body["buildDate"] == "2026-10-14T18:00:00Z"


def test_ready_returns_503_when_database_is_unreachable() -> None:
    settings = Settings(
        _env_file=None,
        app_env="ci",
        database_url=PostgresDsn("postgresql+psycopg://user:pw@127.0.0.1:1/nowhere"),
    )

    with TestClient(create_app(settings)) as client:
        response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {"status": "unavailable", "checks": {"database": "error"}}


def test_unknown_route_returns_404(client: TestClient) -> None:
    response = client.get("/does-not-exist")

    assert response.status_code == 404
