from typing import Annotated, Tuple

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cores.database import Base
from app.endpoints import endpoint
from app.models.project_ownership import ProjectOwnership
from app.models.project_permission import ProjectPermission
from app.models.project_sharing import ProjectSharing
from app.models.projects import Projects
from app.repositories.database_repository import DatabaseRepository


def get_shared_session(
    session: AsyncSession = Depends(endpoint.postgres.db_session),
) -> AsyncSession:
    return session


def get_repository(
    model: type[Base],
    session: Annotated[AsyncSession, Depends(get_shared_session)],
) -> DatabaseRepository:
    return DatabaseRepository(model, session)


ProjectRepository = Annotated[
    DatabaseRepository[Projects],
    Depends(lambda session: get_repository(Projects, session)),
]

ProjectOwnershipRepository = Annotated[
    DatabaseRepository[ProjectOwnership],
    Depends(lambda session: get_repository(ProjectOwnership, session)),
]

ProjectPermissionRepository = Annotated[
    DatabaseRepository[ProjectPermission],
    Depends(lambda session: get_repository(ProjectPermission, session)),
]

ProjectSharingRepository = Annotated[
    DatabaseRepository[ProjectSharing],
    Depends(lambda session: get_repository(ProjectSharing, session)),
]


def get_project_bundle_repo(
    projects_repo: ProjectRepository,
    project_ownership_repo: ProjectOwnershipRepository,
    project_permission_repo: ProjectPermissionRepository,
    project_sharing_repo: ProjectSharingRepository,
) -> Tuple[
    DatabaseRepository[Projects],
    DatabaseRepository[ProjectOwnership],
    DatabaseRepository[ProjectPermission],
    DatabaseRepository[ProjectSharing],
]:
    return (
        projects_repo,
        project_ownership_repo,
        project_permission_repo,
        project_sharing_repo,
    )


ProjectBundleRepository = Annotated[
    Tuple[
        DatabaseRepository[Projects],
        DatabaseRepository[ProjectOwnership],
        DatabaseRepository[ProjectPermission],
        DatabaseRepository[ProjectSharing],
    ],
    Depends(get_project_bundle_repo),
]
