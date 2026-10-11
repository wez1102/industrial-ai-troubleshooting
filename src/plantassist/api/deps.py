from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from plantassist.db.repositories.incidents import SqlIncidentRepository
from plantassist.services.incidents import IncidentService


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    """
    Provide one database session per request and always close it.
    """
    session_factory: async_sessionmaker[AsyncSession] = request.app.state.session_factory
    async with session_factory() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_incident_service(session: SessionDep) -> IncidentService:
    """
    Build the service for this request, on this request's session.
    """
    return IncidentService(SqlIncidentRepository(session), session)


IncidentServiceDep = Annotated[IncidentService, Depends(get_incident_service)]
