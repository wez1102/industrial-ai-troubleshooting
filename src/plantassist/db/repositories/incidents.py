from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from plantassist.db.models import Incident
from plantassist.domain.incidents import IncidentFilters


class SqlIncidentRepository:
    """
    Stores and queries incidents in PostgreSQL.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, incident: Incident) -> None:
        """
        Stage a new incident and send the INSERT (not committed yet).
        """
        self._session.add(incident)
        await self._session.flush()

    async def get(self, incident_id: UUID) -> Incident | None:
        """
        Return the incident with this ID, or None.
        """
        return await self._session.get(Incident, incident_id)

    async def search(
        self, filters: IncidentFilters, *, limit: int, offset: int
    ) -> tuple[list[Incident], int]:
        """
        Return one page of matching incidents (newest first) and the total match count.
        """
        query = self._apply_filters(select(Incident), filters)

        total = await self._session.scalar(select(func.count()).select_from(query.subquery()))
        rows = await self._session.scalars(
            query.order_by(Incident.created_at.desc(), Incident.id).limit(limit).offset(offset)
        )
        return list(rows), total or 0

    @staticmethod
    def _apply_filters(query: Select[Incident], filters: IncidentFilters) -> Select[Incident]:
        if filters.status is not None:
            query = query.where(Incident.status == filters.status)
        if filters.machine_id is not None:
            query = query.where(Incident.machine_id == filters.machine_id)
        if filters.alarm_code is not None:
            query = query.where(Incident.alarm_code == filters.alarm_code)
        return query
