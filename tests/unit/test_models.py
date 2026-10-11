import pytest

import plantassist.db.models  # noqa: F401  (registers the models on Base.metadata)
from plantassist.db.base import Base

pytestmark = pytest.mark.unit


def test_incidents_table_uses_naming_convention() -> None:
    table = Base.metadata.tables["incidents"]

    constraint_names = {constraint.name for constraint in table.constraints}
    index_names = {index.name for index in table.indexes}

    assert {"pk_incidents", "ck_incidents_status_valid"} <= constraint_names
    assert index_names == {
        "ix_incidents_machine_id",
        "ix_incidents_alarm_code",
        "ix_incidents_status",
    }
