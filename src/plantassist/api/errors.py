from collections.abc import Mapping
from datetime import UTC, datetime
from typing import cast

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from plantassist.api.schemas.base import ApiModel
from plantassist.domain.incidents import IncidentNotFoundError, InvalidStatusTransitionError
from plantassist.observability.request_id import get_request_id


class FieldError(ApiModel):
    field: str
    message: str


class ErrorResponse(ApiModel):
    """
    The body of every error response.
    """

    timestamp: datetime
    status: int
    code: str
    message: str
    request_id: str | None = None
    details: list[FieldError] | None = None


# Domain error → (HTTP status, stable error code). The domain itself knows nothing about HTTP.
DOMAIN_ERRORS: dict[type[Exception], tuple[int, str]] = {
    IncidentNotFoundError: (status.HTTP_404_NOT_FOUND, "INCIDENT_NOT_FOUND"),
    InvalidStatusTransitionError: (status.HTTP_409_CONFLICT, "INVALID_STATUS_TRANSITION"),
}

HTTP_ERROR_CODES = {
    status.HTTP_404_NOT_FOUND: "NOT_FOUND",
    status.HTTP_405_METHOD_NOT_ALLOWED: "METHOD_NOT_ALLOWED",
}


def error_response(
    status_code: int,
    code: str,
    message: str,
    details: list[FieldError] | None = None,
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    """
    Build a response in the standard error shape.
    """
    body = ErrorResponse(
        timestamp=datetime.now(UTC),
        status=status_code,
        code=code,
        message=message,
        request_id=get_request_id(),
        details=details,
    )
    return JSONResponse(
        status_code=status_code,
        content=body.model_dump(mode="json", by_alias=True, exclude_none=True),
        headers=headers,
    )


async def handle_domain_error(request: Request, exc: Exception) -> JSONResponse:
    status_code, code = DOMAIN_ERRORS[type(exc)]
    return error_response(status_code, code, str(exc))


async def handle_validation_error(request: Request, exc: Exception) -> JSONResponse:
    details = [
        FieldError(field=".".join(str(part) for part in error["loc"]), message=error["msg"])
        for error in cast(RequestValidationError, exc).errors()
    ]
    return error_response(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        "VALIDATION_ERROR",
        "Request validation failed",
        details,
    )


async def handle_http_error(request: Request, exc: Exception) -> JSONResponse:
    http_exc = cast(StarletteHTTPException, exc)
    code = HTTP_ERROR_CODES.get(http_exc.status_code, "HTTP_ERROR")
    return error_response(
        http_exc.status_code, code, str(http_exc.detail), headers=http_exc.headers
    )


def register_error_handlers(app: FastAPI) -> None:
    """
    Attach every error handler to the app.
    """
    for exc_type in DOMAIN_ERRORS:
        app.add_exception_handler(exc_type, handle_domain_error)
    app.add_exception_handler(RequestValidationError, handle_validation_error)
    app.add_exception_handler(StarletteHTTPException, handle_http_error)
