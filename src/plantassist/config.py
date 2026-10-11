from functools import lru_cache
from typing import Literal

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application base settings, loaded from the envoriment variables and .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "PlantAssist AI"
    app_env: Literal["local", "ci", "staging", "production"] = "local"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    database_url: PostgresDsn = PostgresDsn(
        "postgresql+psycopg://plantassist:plantassist@localhost:5432/plantassist"
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return one shared Settings instance for the whole application.
    """
    return Settings()
