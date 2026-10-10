import uuid
from datetime import UTC, datetime
from typing import Any

import pytest
from pydantic import ValidationError

from plantassist.api.schemas.incidents import IncidentCreate, IncidentRead
from plantassist.db.models import Incident
from plantassist.domain.incidents import IncidentStatus

pytestmark = pytest.mark.unit


def valid_create_payload() -> dict[str, Any]:
    return {
        "machineId": "CP-01",
        "alarmCode": "SERVO-7021",
        "title": "Servo axis 4 following error",
        "symptoms": "Fault occurs during rapid acceleration.",
    }


def test_create_accepts_camel_case_json() -> None:
    incident = IncidentCreate.model_validate(valid_create_payload())

    assert incident.machine_id == "CP-01"
    assert incident.alarm_code == "SERVO-7021"


def test_create_strips_surrounding_whitespace() -> None:
    payload = valid_create_payload() | {"title": "  Servo fault  "}

    assert IncidentCreate.model_validate(payload).title == "Servo fault"


@pytest.mark.parametrize(
    ("field", "bad_value"),
    [
        ("title", "   "),
        ("title", "x" * 201),
        ("machineId", ""),
        ("machineId", "x" * 65),
        ("symptoms", ""),
    ],
)
def test_create_rejects_invalid_fields(field: str, bad_value: str) -> None:
    payload = valid_create_payload() | {field: bad_value}

    with pytest.raises(ValidationError):
        IncidentCreate.model_validate(payload)


def test_alarm_code_is_optional() -> None:
    payload = valid_create_payload()
    del payload["alarmCode"]

    assert IncidentCreate.model_validate(payload).alarm_code is None


def test_read_model_serializes_orm_incident_as_camel_case() -> None:
    now = datetime.now(UTC)
    orm_incident = Incident(
        id=uuid.uuid4(),
        machine_id="CP-01",
        alarm_code=None,
        title="Servo fault",
        symptoms="Following error",
        status="OPEN",
        resolution=None,
        created_at=now,
        updated_at=now,
        resolved_at=None,
    )

    data = IncidentRead.model_validate(orm_incident).model_dump(mode="json", by_alias=True)

    assert data["machineId"] == "CP-01"
    assert data["status"] == IncidentStatus.OPEN
    assert "machine_id" not in data
