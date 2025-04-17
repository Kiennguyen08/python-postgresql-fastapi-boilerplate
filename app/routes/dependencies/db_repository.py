from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cores.database import Base
from app.endpoints import endpoint
from app.models.message import Message
from app.repositories.database_repository import DatabaseRepository


def get_repository(
    model: type[Base],
    session: AsyncSession,
) -> DatabaseRepository:
    return DatabaseRepository(model, session)


def get_message_repository(
    db: AsyncSession = Depends(endpoint.postgres.db_session),
) -> DatabaseRepository[Message]:
    return get_repository(Message, db)
