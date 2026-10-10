import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from plantassist.config import Settings
from plantassist.main import create_app

pytestmark = pytest.mark.unit


def test_startup_creates_session_factory(settings: Settings) -> None:
    app = create_app(settings)

    with TestClient(app):
        assert isinstance(app.state.session_factory, async_sessionmaker)
