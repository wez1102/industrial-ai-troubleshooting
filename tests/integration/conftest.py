import os
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import pytest
import sqlalchemy as sa
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncSession
from testcontainers.community.postgres import PostgresContainer

from plantassist.config import get_settings
from plantassist.db.session import create_engine, create_session_factory

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def migrated_database_url() -> Iterator[str]:
    """
    Start a throwaway Postgres once per test run and apply all migrations.
    """
    with PostgresContainer("pgvector/pgvector:pg17", driver="psycopg") as postgres:
        url = postgres.get_connection_url()

        previous = os.environ.get("DATABASE_URL")
        os.environ["DATABASE_URL"] = url
        get_settings.cache_clear()
        try:
            command.upgrade(Config(str(PROJECT_ROOT / "alembic.ini")), "head")
        finally:
            if previous is None:
                os.environ.pop("DATABASE_URL", None)
            else:
                os.environ["DATABASE_URL"] = previous
            get_settings.cache_clear()

        yield url


@pytest.fixture
def database_url(migrated_database_url: str) -> str:
    """
    The test database URL, emptied before each test.
    """
    engine = sa.create_engine(migrated_database_url)
    with engine.begin() as connection:
        connection.execute(sa.text("TRUNCATE incidents"))
    engine.dispose()
    return migrated_database_url


@pytest.fixture
async def session(database_url: str) -> AsyncIterator[AsyncSession]:
    """
    A real async session on the test database.
    """
    engine = create_engine(database_url)
    async with create_session_factory(engine)() as db_session:
        yield db_session
    await engine.dispose()
