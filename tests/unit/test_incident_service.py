import uuid
from datetime import UTC, datetime
from uuid import UUID

import pytest

from plantassist.db.models import Incident
from plantassist.domain.incidents import (
    IncidentFilters,
    IncidentNotFoundError,
    IncidentStatus,
    InvalidStatusTransitionError,
)
from plantassist.services.incidents import IncidentService

pytestmark = [pytest.mark.unit, pytest.mark.anyio]


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


@pytest.fixture
def repository() -> FakeIncidentRepository:
    return FakeIncidentRepository()


@pytest.fixture
def transaction() -> FakeTransaction:
    return FakeTransaction()


@pytest.fixture
def service(repository: FakeIncidentRepository, transaction: FakeTransaction) -> IncidentService:
    return IncidentService(repository, transaction)


async def create_incident(service: IncidentService, machine_id: str = "CP-01") -> Incident:
    return await service.create(
        machine_id=machine_id,
        alarm_code="SERVO-7021",
        title="Servo axis 4 following error",
        symptoms="Fault during rapid acceleration",
    )


async def test_create_opens_incident_and_commits(
    service: IncidentService,
    repository: FakeIncidentRepository,
    transaction: FakeTransaction,
) -> None:
    incident = await create_incident(service)

    assert incident.status == IncidentStatus.OPEN
    assert incident.id in repository.incidents
    assert transaction.commits == 1


async def test_get_missing_incident_raises_not_found(service: IncidentService) -> None:
    missing_id = uuid.uuid4()

    with pytest.raises(IncidentNotFoundError) as exc_info:
        await service.get(missing_id)

    assert exc_info.value.incident_id == missing_id


async def test_record_resolution_resolves_incident(
    service: IncidentService, transaction: FakeTransaction
) -> None:
    incident = await create_incident(service)

    resolved = await service.record_resolution(incident.id, "Encoder connector was loose.")

    assert resolved.status == IncidentStatus.RESOLVED
    assert resolved.resolution == "Encoder connector was loose."
    assert resolved.resolved_at is not None
    assert transaction.commits == 2  # create + resolve


async def test_cannot_resolve_closed_incident(
    service: IncidentService, transaction: FakeTransaction
) -> None:
    incident = await create_incident(service)
    incident.status = IncidentStatus.CLOSED

    with pytest.raises(InvalidStatusTransitionError):
        await service.record_resolution(incident.id, "Too late")

    assert transaction.commits == 1  # only the create; the failed resolve committed nothing


async def test_list_returns_requested_page_and_total(service: IncidentService) -> None:
    for _ in range(3):
        await create_incident(service)

    first_page, total = await service.list_incidents(IncidentFilters(), page=1, size=2)
    second_page, _ = await service.list_incidents(IncidentFilters(), page=2, size=2)

    assert total == 3
    assert len(first_page) == 2
    assert len(second_page) == 1


async def test_list_filters_by_machine(service: IncidentService) -> None:
    await create_incident(service, machine_id="CP-01")
    await create_incident(service, machine_id="CV-02")

    items, total = await service.list_incidents(
        IncidentFilters(machine_id="CV-02"), page=1, size=10
    )

    assert total == 1
    assert items[0].machine_id == "CV-02"
