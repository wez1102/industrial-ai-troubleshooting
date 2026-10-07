from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from plantassist.config import Settings, get_settings
from plantassist.main import create_app

@pytest.fixture
def settings() -> Settings:
    """
    Settings for tests: ignore the dev's .env file.
    """
    return Settings(_env_file=None, app_env="ci")

@pytest.fixture
def client(settings: Settings) -> Iterator[TestClient]:
    """
    A test client for a fresh app that uses the test settings.
    """
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: settings
    with TestClient(app) as test_client:
        yield test_client
