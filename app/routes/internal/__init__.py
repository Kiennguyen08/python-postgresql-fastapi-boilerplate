from fastapi import APIRouter

from app.routes.health_route import heath_router

internal_router = APIRouter()

# internal api
internal_router.include_router(heath_router, tags=["health"])
