import uuid

import pytest
from fakes import FakeIncidentRepository, FakeTransaction

from plantassist.db.models import Incident
from plantassist.domain.incidents import (
    IncidentFilters,
    IncidentNotFoundError,
    IncidentStatus,
    InvalidStatusTransitionError,
)
from plantassist.services.incidents import IncidentService

pytestmark = [pytest.mark.unit, pytest.mark.anyio]


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
