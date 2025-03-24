import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.models.project_ownership import ProjectOwnership
from app.models.project_permission import ProjectPermission
from app.models.project_sharing import ProjectSharing
from app.models.projects import Projects
from app.repositories.database_repository import DatabaseRepository
from app.services.project_service import ProjectService


@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def database_url():
    return "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
async def engine(database_url):
    engine = create_async_engine(database_url, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Projects.metadata.drop_all)
        await conn.run_sync(ProjectOwnership.metadata.drop_all)
        await conn.run_sync(ProjectPermission.metadata.drop_all)
        await conn.run_sync(ProjectSharing.metadata.drop_all)
        await conn.run_sync(Projects.metadata.create_all)
        await conn.run_sync(ProjectOwnership.metadata.create_all)
        await conn.run_sync(ProjectPermission.metadata.create_all)
        await conn.run_sync(ProjectSharing.metadata.create_all)
    return engine


@pytest.fixture(scope="session")
async def session_maker(engine):
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
async def session(session_maker):
    async with session_maker() as session:
        yield session


@pytest.fixture(scope="session")
async def repositories(session):
    projects_repo = DatabaseRepository(Projects, session)
    project_ownership_repo = DatabaseRepository(ProjectOwnership, session)
    project_permission_repo = DatabaseRepository(ProjectPermission, session)
    project_sharing_repo = DatabaseRepository(ProjectSharing, session)
    return (
        projects_repo,
        project_ownership_repo,
        project_permission_repo,
        project_sharing_repo,
    )


@pytest.fixture(scope="session")
async def integration_project_service(repositories):
    return ProjectService(repositories)
