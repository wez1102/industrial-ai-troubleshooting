from importlib.metadata import version
from typing import Annotated, Literal

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from plantassist.config import Settings, get_settings

router = APIRouter(tags=["healthy"])

class LiveResponse(BaseModel):
    status: Literal["ok"]

class VersionResponse(BaseModel):
    name: str
    version: str
    enviroment: str

@router.get("/health/live")
def live() -> LiveResponse:
    """
    Liveness probe: the process is setup and can answer questions.
    """
    return LiveResponse(status="ok")

@router.get("/version")
def get_version(settings: Annotated[Settings, Depends(get_settings)],) -> VersionResponse:
    """
    Report which build of the app is running.
    """
    return VersionResponse(
        name=settings.app_name,
        version=version("plantassist"),
        enviroment=settings.app_env,
    )