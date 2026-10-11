from datetime import UTC, datetime
from typing import Protocol
from uuid import UUID

from plantassist.db.models import Incident
from plantassist.domain.incidents import (
    IncidentFilters,
    IncidentNotFoundError,
    IncidentStatus,
    ensure_transition,
)


class IncidentRepository(Protocol):
    """
    What the service needs from storage. SqlIncidentRepository satisfies this.
    """

    async def add(self, incident: Incident) -> None: ...

    async def get(self, incident_id: UUID) -> Incident | None: ...

    async def search(
        self, filters: IncidentFilters, *, limit: int, offset: int
    ) -> tuple[list[Incident], int]: ...


class Transaction(Protocol):
    """
    Something that can make the current unit of work permanent. AsyncSession satisfies this.
    """

    async def commit(self) -> None: ...


class IncidentService:
    """
    Business operations on incidents. The only place that commits.
    """

    def __init__(self, repository: IncidentRepository, transaction: Transaction) -> None:
        self._repository = repository
        self._transaction = transaction

    async def create(
        self, *, machine_id: str, alarm_code: str | None, title: str, symptoms: str
    ) -> Incident:
        incident = Incident(
            machine_id=machine_id,
            alarm_code=alarm_code,
            title=title,
            symptoms=symptoms,
            status=IncidentStatus.OPEN,
        )
        await self._repository.add(incident)
        await self._transaction.commit()
        return incident

    async def get(self, incident_id: UUID) -> Incident:
        incident = await self._repository.get(incident_id)
        if incident is None:
            raise IncidentNotFoundError(incident_id)
        return incident

    async def list_incidents(
        self, filters: IncidentFilters, *, page: int, size: int
    ) -> tuple[list[Incident], int]:
        return await self._repository.search(filters, limit=size, offset=(page - 1) * size)

    async def record_resolution(self, incident_id: UUID, resolution: str) -> Incident:
        incident = await self.get(incident_id)
        ensure_transition(IncidentStatus(incident.status), IncidentStatus.RESOLVED)

        incident.status = IncidentStatus.RESOLVED
        incident.resolution = resolution
        incident.resolved_at = datetime.now(UTC)

        await self._transaction.commit()
        return incident
