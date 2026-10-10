import itertools

import pytest

import plantassist.db.models  # noqa: F401  (registers the models on Base.metadata)
from plantassist.db.base import Base
from plantassist.domain.incidents import (
    IncidentStatus,
    InvalidStatusTransitionError,
    can_transition,
    ensure_transition,
)

pytestmark = pytest.mark.unit

OPEN = IncidentStatus.OPEN
IN_PROGRESS = IncidentStatus.IN_PROGRESS
RESOLVED = IncidentStatus.RESOLVED
CLOSED = IncidentStatus.CLOSED

# The business rules, written out independently of the implementation.
EXPECTED_ALLOWED = {
    (OPEN, IN_PROGRESS),
    (OPEN, RESOLVED),
    (OPEN, CLOSED),
    (IN_PROGRESS, OPEN),
    (IN_PROGRESS, RESOLVED),
    (IN_PROGRESS, CLOSED),
    (RESOLVED, IN_PROGRESS),
    (RESOLVED, CLOSED),
}


@pytest.mark.parametrize(("current", "target"), list(itertools.product(IncidentStatus, repeat=2)))
def test_can_transition_matches_business_rules(
    current: IncidentStatus, target: IncidentStatus
) -> None:
    assert can_transition(current, target) is ((current, target) in EXPECTED_ALLOWED)


def test_closed_is_final() -> None:
    assert not any(can_transition(CLOSED, target) for target in IncidentStatus)


def test_ensure_transition_rejects_invalid_move() -> None:
    with pytest.raises(InvalidStatusTransitionError) as exc_info:
        ensure_transition(CLOSED, OPEN)

    assert exc_info.value.current is CLOSED
    assert exc_info.value.target is OPEN


def test_statuses_match_database_check_constraint() -> None:
    table = Base.metadata.tables["incidents"]
    check = next(c for c in table.constraints if c.name == "ck_incidents_status_valid")
    constraint_sql = str(check.sqltext)  # type: ignore[attr-defined]

    for status in IncidentStatus:
        assert f"'{status.value}'" in constraint_sql
