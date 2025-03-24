from unittest.mock import AsyncMock, MagicMock

import pytest

from app.constants.enum import ProjectPermission as Permission
from app.cores.errors import BadRequestException
from app.dto.requests.project import CreateProjectRequest
from app.models.project_permission import ProjectPermission
from app.models.projects import Projects
from app.services.project_service import ProjectService


@pytest.fixture
def mock_repositories():
    projects_repo = AsyncMock()
    project_ownership_repo = AsyncMock()
    project_permission_repo = AsyncMock()
    project_sharing_repo = AsyncMock()
    return (
        projects_repo,
        project_ownership_repo,
        project_permission_repo,
        project_sharing_repo,
    )


@pytest.fixture
def project_service(mock_repositories):
    return ProjectService(mock_repositories)


@pytest.mark.asyncio
async def test_list_projects(project_service, mock_repositories):
    user_id = "test_user_id"
    search = "test_search"
    created_at_from = 1633072800
    created_at_to = 1633159200
    skip = 0
    limit = 10

    mock_project_permission_entities = [
        MagicMock(project_id=1),
        MagicMock(project_id=2),
    ]
    mock_projects_repo = mock_repositories[0]
    mock_project_permission_repo = mock_repositories[2]

    mock_project_permission_repo.filter.return_value = mock_project_permission_entities
    mock_projects_repo.filter.return_value = [
        Projects(id=1, name="Project 1"),
        Projects(id=2, name="Project 2"),
    ]
    mock_projects_repo.count.return_value = 2

    entities, total_item_searched = await project_service.list_projects(
        user_id, search, created_at_from, created_at_to, skip, limit
    )

    assert len(entities) == 2
    assert total_item_searched == 2


@pytest.mark.asyncio
async def test_integration_list_projects(integration_project_service, session):
    # Create test data
    user_id = "test_user"
    project1 = Projects(name="Project 1", description="Description 1")
    project2 = Projects(name="Project 2", description="Description 2")
    session.add_all([project1, project2])
    await session.flush()
    project_permission1 = ProjectPermission(
        user_id=user_id, project_id=project1.id, permission_type=Permission.EDIT
    )
    project_permission2 = ProjectPermission(
        user_id=user_id, project_id=project2.id, permission_type=Permission.VIEW
    )
    session.add_all([project_permission1, project_permission2])
    await session.commit()

    # Test listing projects
    projects, total = await integration_project_service.list_projects(user_id, "")
    assert total == 2
    assert len(projects) == 2


@pytest.mark.asyncio
async def test_integration_create_project(integration_project_service, session):
    print("integration_project_service", integration_project_service)
    user_id = "test_user"
    request = CreateProjectRequest(name="New Project", description="New Description")

    # Test creating a new project
    new_project = await integration_project_service.create_project(user_id, request)
    assert new_project.name == "New Project"
    assert new_project.description == "New Description"

    # Test creating a duplicate project
    with pytest.raises(BadRequestException):
        await integration_project_service.create_project(user_id, request)
