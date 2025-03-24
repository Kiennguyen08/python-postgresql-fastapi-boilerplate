from fastapi import APIRouter

from app.routes.health_route import heath_router

from .project_route import internal_project_router

internal_router = APIRouter()

# internal api
internal_router.include_router(heath_router, tags=["health"])
internal_router.include_router(internal_project_router, tags=["projects"])
