from enum import StrEnum


class IncidentStatus(StrEnum):
    """
    Lifecycle of an incident. Values must match the DB check constraint.
    """

    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


ALLOWED_TRANSITIONS: dict[IncidentStatus, frozenset[IncidentStatus]] = {
    IncidentStatus.OPEN: frozenset(
        {IncidentStatus.IN_PROGRESS, IncidentStatus.RESOLVED, IncidentStatus.CLOSED}
    ),
    IncidentStatus.IN_PROGRESS: frozenset(
        {IncidentStatus.OPEN, IncidentStatus.RESOLVED, IncidentStatus.CLOSED}
    ),
    IncidentStatus.RESOLVED: frozenset({IncidentStatus.IN_PROGRESS, IncidentStatus.CLOSED}),
    IncidentStatus.CLOSED: frozenset(),
}


class InvalidStatusTransitionError(Exception):
    """
    Raised when an incident is asked to move to a status it can't reach.
    """

    def __init__(self, current: IncidentStatus, target: IncidentStatus) -> None:
        super().__init__(f"Cannot change incident status from {current} to {target}")
        self.current = current
        self.target = target


def can_transition(current: IncidentStatus, target: IncidentStatus) -> bool:
    """
    Return True if an incident may move from `current` to `target`.
    """
    return target in ALLOWED_TRANSITIONS[current]


def ensure_transition(current: IncidentStatus, target: IncidentStatus) -> None:
    """
    Raise InvalidStatusTransitionError if the move isn't allowed.
    """
    if not can_transition(current, target):
        raise InvalidStatusTransitionError(current, target)
