from importlib.metadata import version

from fastapi import FastAPI

from plantassist.api.routers import health
from plantassist.config import get_settings


def create_app() -> FastAPI:
    """
    Build and configure the FastAPI application.
    """

    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=version("plantassist"),
    )

    app.include_router(health.router)

    return app
