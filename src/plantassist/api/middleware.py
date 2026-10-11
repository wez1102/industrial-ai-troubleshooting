import logging
from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status

from plantassist.api.errors import error_response
from plantassist.observability.request_id import (
    REQUEST_ID_HEADER,
    choose_request_id,
    request_id_var,
)

logger = logging.getLogger(__name__)


async def request_id_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    Tag every request with an ID and turn unexpected crashes into a safe 500.
    """
    request_id = choose_request_id(request.headers.get(REQUEST_ID_HEADER))
    token = request_id_var.set(request_id)
    try:
        try:
            response = await call_next(request)
        except Exception:
            logger.exception("Unhandled error in request %s", request_id)
            response = error_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "INTERNAL_ERROR",
                "An unexpected error occurred.",
            )
        response.headers[REQUEST_ID_HEADER] = request_id
        return response
    finally:
        request_id_var.reset(token)
