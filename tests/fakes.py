import uuid
from datetime import UTC, datetime
from uuid import UUID

from plantassist.db.models import Incident
from plantassist.domain.incidents import IncidentFilters


class FakeIncidentRepository:
    """
    In-memory stand-in that behaves like the real repository.
    """

    def __init__(self) -> None:
        self.incidents: dict[UUID, Incident] = {}

    async def add(self, incident: Incident) -> None:
        # Mimic what the database does on INSERT.
        now = datetime.now(UTC)
        incident.id = uuid.uuid4()
        incident.created_at = now
        incident.updated_at = now
        self.incidents[incident.id] = incident

    async def get(self, incident_id: UUID) -> Incident | None:
        return self.incidents.get(incident_id)

    async def search(
        self, filters: IncidentFilters, *, limit: int, offset: int
    ) -> tuple[list[Incident], int]:
        matches = [
            incident
            for incident in self.incidents.values()
            if (filters.status is None or incident.status == filters.status)
            and (filters.machine_id is None or incident.machine_id == filters.machine_id)
            and (filters.alarm_code is None or incident.alarm_code == filters.alarm_code)
        ]
        matches.sort(key=lambda incident: incident.created_at, reverse=True)
        return matches[offset : offset + limit], len(matches)


class FakeTransaction:
    """
    Counts commits so tests can check the unit of work.
    """

    def __init__(self) -> None:
        self.commits = 0

    async def commit(self) -> None:
        self.commits += 1
