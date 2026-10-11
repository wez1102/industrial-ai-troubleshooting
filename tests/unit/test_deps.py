from contextlib import asynccontextmanager
from types import SimpleNamespace

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from plantassist.api.deps import get_session
from plantassist.config import Settings
from plantassist.db.session import create_engine, create_session_factory

pytestmark = [pytest.mark.unit, pytest.mark.anyio]


async def test_get_session_yields_session_from_app_factory(settings: Settings) -> None:
    engine = create_engine(str(settings.database_url))
    app = SimpleNamespace(state=SimpleNamespace(session_factory=create_session_factory(engine)))
    request = Request({"type": "http", "app": app})

    try:
        async with asynccontextmanager(get_session)(request) as session:
            assert isinstance(session, AsyncSession)
    finally:
        await engine.dispose()
