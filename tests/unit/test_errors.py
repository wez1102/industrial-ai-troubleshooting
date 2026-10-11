import pytest
from fastapi.testclient import TestClient

from plantassist.config import Settings
from plantassist.main import create_app

pytestmark = pytest.mark.unit


def test_generates_request_id_when_none_is_sent(client: TestClient) -> None:
    response = client.get("/health/live")

    assert len(response.headers["X-Request-ID"]) == 32


def test_echoes_a_safe_incoming_request_id(client: TestClient) -> None:
    response = client.get("/health/live", headers={"X-Request-ID": "trace-abc.123"})

    assert response.headers["X-Request-ID"] == "trace-abc.123"


def test_replaces_an_unsafe_incoming_request_id(client: TestClient) -> None:
    response = client.get("/health/live", headers={"X-Request-ID": "not safe!"})

    assert response.headers["X-Request-ID"] != "not safe!"


def test_unknown_route_uses_standard_error_shape(client: TestClient) -> None:
    response = client.get("/does-not-exist")
    body = response.json()

    assert response.status_code == 404
    assert body["code"] == "NOT_FOUND"
    assert body["requestId"] == response.headers["X-Request-ID"]
    assert {"timestamp", "status", "code", "message", "requestId"} <= body.keys()


def test_unexpected_error_returns_safe_500(settings: Settings) -> None:
    app = create_app(settings)

    async def crash() -> None:
        raise RuntimeError("connection string with secret details")

    app.add_api_route("/crash", crash)

    with TestClient(app) as test_client:
        response = test_client.get("/crash")

    assert response.status_code == 500
    assert response.json()["code"] == "INTERNAL_ERROR"
    assert "secret" not in response.text
    assert "X-Request-ID" in response.headers
