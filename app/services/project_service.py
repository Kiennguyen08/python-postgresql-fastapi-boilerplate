from typing import Optional, Tuple

from sqlalchemy import or_

from app.constants.enum import ProjectPermission as Permission
from app.constants.error import ErrorCode
from app.cores.errors import BadRequestException
from app.dto.project import Project
from app.dto.requests.project import CreateProjectRequest
from app.models.project_ownership import ProjectOwnership
from app.models.project_permission import ProjectPermission
from app.models.project_sharing import ProjectSharing
from app.models.projects import Projects
from app.repositories.database_repository import DatabaseRepository


class ProjectService:
    def __init__(
        self,
        repository: Tuple[
            DatabaseRepository[Projects],
            DatabaseRepository[ProjectOwnership],
            DatabaseRepository[ProjectPermission],
            DatabaseRepository[ProjectSharing],
        ],
    ):
        (
            self.projects_repo,
            self.project_ownership_repo,
            self.project_permission_repo,
            self.project_sharing_repo,
        ) = repository

    async def list_projects(
        self,
        user_id: str,
        search: str,
        created_at_from: Optional[int] = None,
        created_at_to: Optional[int] = None,
        skip: int = 0,
        limit: int = 10,
    ):
        filters_by_user_id_permission = [
            ProjectPermission.user_id == user_id,
            ProjectPermission.permission_type.in_([Permission.VIEW, Permission.EDIT]),
        ]
        project_permission_entities = await self.project_permission_repo.filter(
            *filters_by_user_id_permission,
        )
        filters = [
            Projects.id.in_(
                [entity.project_id for entity in project_permission_entities]
            )
        ]

        if search:
            filters.append(
                or_(
                    Projects.name.ilike(f"%{search}%"),
                    Projects.description.ilike(f"%{search}%"),
                )
            )
        if created_at_from:
            filters.append(Projects.created_at >= created_at_from)

        if created_at_to:
            filters.append(Projects.created_at <= created_at_to)

        entities = await self.projects_repo.filter(
            *filters,
            skip=skip,
            limit=limit,
        )
        total_item_searched = await self.projects_repo.count(*filters)
        return entities, total_item_searched

    async def create_project(self, user_id: str, request: CreateProjectRequest):
        is_duplicated = await self.find_duplicate_project_name(user_id, request.name)
        if is_duplicated:
            raise BadRequestException(ErrorCode.PROJECT_NAME_ALREADY_EXISTED.value)
        shared_session = self.projects_repo.session
        new_project = Projects(name=request.name, description=request.description)
        shared_session.add(new_project)
        await shared_session.flush()  # Flush to get the new_project.id
        project_ownership = ProjectOwnership(
            user_id=user_id,
            project_id=new_project.id,
        )
        shared_session.add(project_ownership)
        project_permission = ProjectPermission(
            user_id=user_id,
            project_id=new_project.id,
            permission_type=Permission.EDIT,
        )
        shared_session.add(project_permission)
        await shared_session.commit()  # Commit all changes
        return Project.model_validate(new_project)

    async def find_duplicate_project_name(self, user_id: str, project_name: str):
        filters_by_user_id_permission = [
            ProjectPermission.user_id == user_id,
            ProjectPermission.permission_type.in_([Permission.VIEW, Permission.EDIT]),
        ]
        project_permission_entities = await self.project_permission_repo.filter(
            *filters_by_user_id_permission,
        )
        filters = [
            Projects.id.in_(
                [entity.project_id for entity in project_permission_entities]
            ),
            Projects.name == project_name,
        ]
        results = await self.projects_repo.count(*filters)
        return results > 0
