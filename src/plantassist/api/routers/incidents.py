from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from plantassist.api.deps import IncidentServiceDep
from plantassist.api.schemas.incidents import (
    IncidentCreate,
    IncidentPage,
    IncidentRead,
    IncidentResolution,
)
from plantassist.domain.incidents import (
    IncidentFilters,
    IncidentNotFoundError,
    IncidentStatus,
    InvalidStatusTransitionError,
)

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_incident(body: IncidentCreate, service: IncidentServiceDep) -> IncidentRead:
    """
    Report a new incident. It starts in status OPEN.
    """
    incident = await service.create(
        machine_id=body.machine_id,
        alarm_code=body.alarm_code,
        title=body.title,
        symptoms=body.symptoms,
    )
    return IncidentRead.model_validate(incident)


@router.get("/{incident_id}")
async def get_incident(incident_id: UUID, service: IncidentServiceDep) -> IncidentRead:
    """
    Fetch one incident by ID.
    """
    try:
        incident = await service.get(incident_id)
    except IncidentNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return IncidentRead.model_validate(incident)


@router.get("")
async def list_incidents(
    service: IncidentServiceDep,
    status_filter: Annotated[IncidentStatus | None, Query(alias="status")] = None,
    machine_id: Annotated[str | None, Query(alias="machineId", max_length=64)] = None,
    alarm_code: Annotated[str | None, Query(alias="alarmCode", max_length=64)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> IncidentPage:
    """
    List incidents, newest first, with optional filters and paging.
    """
    filters = IncidentFilters(status=status_filter, machine_id=machine_id, alarm_code=alarm_code)
    items, total = await service.list_incidents(filters, page=page, size=size)
    return IncidentPage(
        items=[IncidentRead.model_validate(item) for item in items],
        total=total,
        page=page,
        size=size,
    )


@router.patch("/{incident_id}/resolution")
async def record_resolution(
    incident_id: UUID, body: IncidentResolution, service: IncidentServiceDep
) -> IncidentRead:
    """
    Record what fixed the problem. Moves the incident to RESOLVED.
    """
    try:
        incident = await service.record_resolution(incident_id, body.resolution)
    except IncidentNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidStatusTransitionError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return IncidentRead.model_validate(incident)
