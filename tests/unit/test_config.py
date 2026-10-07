import pytest
from pydantic import ValidationError

from plantassist.config import Settings

pytestmark = pytest.mark.unit


def test_defaults_when_no_enviroment_is_set(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)

    settings = Settings(_env_file=None)

    assert settings.app_env == "local"
    assert settings.log_level == "INFO"


def test_enviroment_variable_override_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "staging")

    assert Settings(_env_file=None).app_env == "staging"


def test_invalid_environment_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "prod")

    with pytest.raises(ValidationError):
        Settings(_env_file=None)
