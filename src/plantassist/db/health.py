import asyncio
import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def database_is_ready(session: AsyncSession, timeout_seconds: float = 2.0) -> bool:
    """Return True if the database answers a trivial query within the timeout."""
    try:
        async with asyncio.timeout(timeout_seconds):
            await session.execute(text("SELECT 1"))
    except Exception:
        # For a probe, any failure (refused, timed out, auth error) simply means "not ready".
        logger.warning("Database readiness check failed", exc_info=True)
        return False
    return True
