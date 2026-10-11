import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from plantassist.db.models import Incident
from plantassist.db.repositories.incidents import SqlIncidentRepository
from plantassist.domain.incidents import IncidentFilters, IncidentStatus
from plantassist.services.incidents import IncidentService

pytestmark = [pytest.mark.integration, pytest.mark.anyio]


def new_incident(machine_id: str = "CP-01", alarm_code: str | None = "SERVO-7021") -> Incident:
    return Incident(
        machine_id=machine_id,
        alarm_code=alarm_code,
        title="Servo axis 4 following error",
        symptoms="Fault during rapid acceleration",
    )


async def test_add_fills_database_defaults(session: AsyncSession) -> None:
    repository = SqlIncidentRepository(session)
    incident = new_incident()

    await repository.add(incident)
    await session.commit()

    # Values the database generated, fetched by eager_defaults without a lazy load.
    assert incident.id is not None
    assert incident.status == "OPEN"
    assert incident.created_at is not None

    assert await repository.get(incident.id) is incident


async def test_search_filters_pages_and_orders_newest_first(session: AsyncSession) -> None:
    repository = SqlIncidentRepository(session)
    for machine_id in ["CP-01", "CP-01", "CV-02"]:
        await repository.add(new_incident(machine_id=machine_id))
        await session.commit()  # separate transactions → distinct created_at values

    page, total = await repository.search(IncidentFilters(machine_id="CP-01"), limit=1, offset=0)
    everything, _ = await repository.search(IncidentFilters(), limit=10, offset=0)

    assert total == 2
    assert len(page) == 1
    assert [i.created_at for i in everything] == sorted(
        (i.created_at for i in everything), reverse=True
    )


async def test_database_rejects_invalid_status(session: AsyncSession) -> None:
    incident = new_incident()
    incident.status = "BROKEN"
    session.add(incident)

    with pytest.raises(IntegrityError):
        await session.flush()


async def test_service_resolves_incident_end_to_end(session: AsyncSession) -> None:
    service = IncidentService(SqlIncidentRepository(session), session)
    created = await service.create(
        machine_id="CP-01", alarm_code=None, title="Servo fault", symptoms="Following error"
    )

    resolved = await service.record_resolution(created.id, "Encoder connector was loose.")

    assert resolved.status == IncidentStatus.RESOLVED
    assert resolved.resolved_at is not None
    assert resolved.updated_at >= resolved.created_at
