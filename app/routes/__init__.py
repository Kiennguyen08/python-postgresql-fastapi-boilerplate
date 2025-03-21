import os

from fastapi import APIRouter

from app.config import config

from .health_route import heath_router
from .internal import internal_router
from .project_route import project_router

build_module = os.getenv("BUILD_MODULE", "public").lower()
router = APIRouter()
public_router = APIRouter()


if build_module == "public":
    public_router.include_router(heath_router, tags=["health"])
    public_router.include_router(project_router, tags=["projects"])
    router.include_router(public_router, prefix=config.metadata.prefix)
elif build_module == "internal":
    router.include_router(internal_router, prefix=config.metadata.prefix)
