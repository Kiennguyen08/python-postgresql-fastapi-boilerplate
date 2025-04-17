import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.models.message import Message
from app.repositories.database_repository import DatabaseRepository


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
        await conn.run_sync(Message.metadata.drop_all)
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
    message_repo = DatabaseRepository(Message, session)
    return (message_repo,)
