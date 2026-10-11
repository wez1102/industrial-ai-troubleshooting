import re
import uuid
from contextvars import ContextVar

REQUEST_ID_HEADER = "X-Request-ID"

_SAFE_REQUEST_ID = re.compile(r"[A-Za-z0-9._-]{1,64}")

request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)


def get_request_id() -> str | None:
    """
    The ID of the request currently being handled, if any.
    """
    return request_id_var.get()


def choose_request_id(incoming: str | None) -> str:
    """
    Reuse a caller's ID if it's safe, otherwise generate a new one.
    """
    if incoming is not None and _SAFE_REQUEST_ID.fullmatch(incoming):
        return incoming
    return uuid.uuid4().hex
