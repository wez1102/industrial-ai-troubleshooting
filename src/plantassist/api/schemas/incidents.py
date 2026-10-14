from datetime import datetime
from uuid import UUID

from pydantic import Field

from plantassist.api.schemas.base import ApiModel
from plantassist.domain.incidents import IncidentStatus


class IncidentCreate(ApiModel):
    """
    Body of POST /api/v1/incidents.
    """

    machine_id: str = Field(min_length=1, max_length=64)
    alarm_code: str | None = Field(default=None, min_length=1, max_length=64)
    title: str = Field(min_length=1, max_length=200)
    symptoms: str = Field(min_length=1, max_length=5000)


class IncidentResolution(ApiModel):
    """
    Body of PATCH /api/v1/incidents/{id}/resolution.
    """

    resolution: str = Field(min_length=1, max_length=5000)


class IncidentRead(ApiModel):
    """
    An incident as returned by the API.
    """

    id: UUID
    machine_id: str
    alarm_code: str | None
    title: str
    symptoms: str
    status: IncidentStatus
    resolution: str | None
    created_at: datetime
    updated_at: datetime
    resolved_at: datetime | None


class IncidentPage(ApiModel):
    """
    One page of a filtered incident list.
    """

    items: list[IncidentRead]
    total: int
    page: int
    size: int
