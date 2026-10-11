from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from importlib.metadata import version

from fastapi import FastAPI

from plantassist.api.errors import register_error_handlers
from plantassist.api.middleware import request_id_middleware
from plantassist.api.routers import health, incidents
from plantassist.config import Settings, get_settings
from plantassist.db.session import create_engine, create_session_factory


def create_app(settings: Settings | None = None) -> FastAPI:
    """
    Build and configure the FastAPI application.
    """

    app_settings = settings or get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        engine = create_engine(str(app_settings.database_url))
        app.state.session_factory = create_session_factory(engine)
        try:
            yield
        finally:
            await engine.dispose()

    app = FastAPI(
        title=app_settings.app_name,
        version=version("plantassist"),
        lifespan=lifespan,
    )
    app.include_router(health.router)
    app.include_router(incidents.router)

    register_error_handlers(app)
    app.middleware("http")(request_id_middleware)

    return app
