from importlib.metadata import version
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Response, status

from plantassist.api.deps import SessionDep
from plantassist.api.schemas.base import ApiModel
from plantassist.config import Settings, get_settings
from plantassist.db.health import database_is_ready

router = APIRouter(tags=["health"])


class LiveResponse(ApiModel):
    status: Literal["ok"]


class ReadyResponse(ApiModel):
    status: Literal["ready", "unavailable"]
    checks: dict[str, Literal["ok", "error"]]


class VersionResponse(ApiModel):
    name: str
    version: str
    environment: str
    git_sha: str
    build_date: str


@router.get("/health/live")
def live() -> LiveResponse:
    """Liveness probe: the process is up and can answer requests."""
    return LiveResponse(status="ok")


@router.get(
    "/health/ready",
    responses={503: {"model": ReadyResponse, "description": "A dependency is unavailable"}},
)
async def ready(session: SessionDep, response: Response) -> ReadyResponse:
    """Readiness probe: the app can serve real traffic (its database answers)."""
    database_ok = await database_is_ready(session)
    if not database_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return ReadyResponse(
        status="ready" if database_ok else "unavailable",
        checks={"database": "ok" if database_ok else "error"},
    )


@router.get("/version")
def get_version(settings: Annotated[Settings, Depends(get_settings)]) -> VersionResponse:
    """Report which build of the app is running."""
    return VersionResponse(
        name=settings.app_name,
        version=version("plantassist"),
        environment=settings.app_env,
        git_sha=settings.git_sha,
        build_date=settings.build_date,
    )
