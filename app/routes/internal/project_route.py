from typing import List, Optional, Tuple

from fastapi import APIRouter, Depends, Query

from app.dto.project import ListProjectResponseData, ProjectResponse
from app.dto.requests.project import CreateProjectInternalRequest
from app.models.project_ownership import ProjectOwnership
from app.models.project_permission import ProjectPermission
from app.models.project_sharing import ProjectSharing
from app.models.projects import Projects
from app.repositories.database_repository import DatabaseRepository
from app.routes.dependencies.db_repository import get_project_repositories
from app.services.project_service import ProjectService

internal_project_router = APIRouter()


def get_repositories() -> Tuple[
    DatabaseRepository[Projects],
    DatabaseRepository[ProjectOwnership],
    DatabaseRepository[ProjectPermission],
    DatabaseRepository[ProjectSharing],
]:
    return get_project_repositories()


@internal_project_router.get(
    "/projects", status_code=200, response_model=ProjectResponse
)
async def list_projects(
    user_id: str,
    repositories: Tuple[
        DatabaseRepository[Projects],
        DatabaseRepository[ProjectOwnership],
        DatabaseRepository[ProjectPermission],
        DatabaseRepository[ProjectSharing],
    ] = Depends(get_project_repositories),
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
):
    project_service = ProjectService(repository=repositories)
    if created_at and len(created_at) == 2:
        from_date, to_date = created_at
    else:
        from_date, to_date = None, None
    projects, total_item_searched = await project_service.list_projects(
        user_id=user_id,
        search=search,
        created_at_from=from_date,
        created_at_to=to_date,
        skip=skip,
        limit=limit,
    )

    return ProjectResponse(
        message="Get voices successfully",
        data=ListProjectResponseData(total_item=total_item_searched, items=projects),
    )


@internal_project_router.post("/projects", status_code=200)
async def create_project(
    body: CreateProjectInternalRequest,
    repositories: Tuple[
        DatabaseRepository[Projects],
        DatabaseRepository[ProjectOwnership],
        DatabaseRepository[ProjectPermission],
        DatabaseRepository[ProjectSharing],
    ] = Depends(get_project_repositories),
):
    project_service = ProjectService(repository=repositories)
    project_data = await project_service.create_project(body.user_id, body)
    return ProjectResponse(message="Create new project successfully", data=project_data)
