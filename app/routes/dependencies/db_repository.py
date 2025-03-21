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


def get_repository(
    model: type[Base],
    session: AsyncSession,
) -> DatabaseRepository:
    return DatabaseRepository(model, session)


def get_project_repository(
    db: AsyncSession = Depends(endpoint.postgres.db_session),
) -> DatabaseRepository[Projects]:
    return get_repository(Projects, db)


def get_project_ownership_repository(
    db: AsyncSession = Depends(endpoint.postgres.db_session),
) -> DatabaseRepository[ProjectOwnership]:
    return get_repository(ProjectOwnership, db)


def get_project_permission_repository(
    db: AsyncSession = Depends(endpoint.postgres.db_session),
) -> DatabaseRepository[ProjectPermission]:
    return get_repository(ProjectPermission, db)


def get_project_sharing_repository(
    db: AsyncSession = Depends(endpoint.postgres.db_session),
) -> DatabaseRepository[ProjectSharing]:
    return get_repository(ProjectSharing, db)


# def get_project_bundle_repo(
#     projects_repo: ProjectRepository,
#     project_ownership_repo: ProjectOwnershipRepository,
#     project_permission_repo: ProjectPermissionRepository,
#     project_sharing_repo: ProjectSharingRepository,
# ) -> Tuple[
#     DatabaseRepository[Projects],
#     DatabaseRepository[ProjectOwnership],
#     DatabaseRepository[ProjectPermission],
#     DatabaseRepository[ProjectSharing],
# ]:
#     return (
#         projects_repo,
#         project_ownership_repo,
#         project_permission_repo,
#         project_sharing_repo,
#     )


# ProjectBundleRepository = Annotated[
#     Tuple[
#         DatabaseRepository[Projects],
#         DatabaseRepository[ProjectOwnership],
#         DatabaseRepository[ProjectPermission],
#         DatabaseRepository[ProjectSharing],
#     ],
#     Depends(get_project_bundle_repo),
# ]
