from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.dto.passport import UserData
from app.dto.project import ListProjectResponseData, ProjectResponse
from app.dto.requests.project import CreateProjectRequest
from app.routes.dependencies.db_repository import ProjectBundleRepository
from app.security.auth import get_current_user
from app.services.project_service import ProjectService

project_router = APIRouter()


@project_router.get("/projects", status_code=200, response_model=ProjectResponse)
async def list_projects(
    project_bundle: ProjectBundleRepository,
    search: Optional[str] = Query(
        None, description="Search by project name or description"
    ),
    skip: Optional[int] = Query(
        0, ge=0, description="Number of records to skip for pagination"
    ),
    limit: Optional[int] = Query(
        10, le=100, description="Number of records to return per page"
    ),
    created_at: Optional[List[int]] = Query(
        None, description="Search by created at date"
    ),
    # user: UserData = Depends(get_current_user),
):
    project_service = ProjectService(project_bundle)
    if created_at and len(created_at) == 2:
        from_date, to_date = created_at
    else:
        from_date, to_date = None, None
    voices, total_item_searched = await project_service.list_projects(
        user_id="user.id",
        search=search,
        created_at_from=from_date,
        created_at_to=to_date,
        skip=skip,
        limit=limit,
    )

    return ProjectResponse(
        message="Get voices successfully",
        data=ListProjectResponseData(total_item=total_item_searched, items=voices),
    )


@project_router.post("/projects", status_code=200)
async def create_project(
    project_bundle: ProjectBundleRepository,
    body: CreateProjectRequest,
    user: UserData = Depends(get_current_user),
):
    project_service = ProjectService(project_bundle)
    project_data = await project_service.create_project(user.id, body)
    return ProjectResponse(message="Create new project successfully", data=project_data)
