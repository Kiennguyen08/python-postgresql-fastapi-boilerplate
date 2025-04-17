from typing import List, Optional, Tuple

from fastapi import APIRouter, Depends, Query


from app.models.message import Message
from app.repositories.database_repository import DatabaseRepository
from app.routes.dependencies.db_repository import get_message_repository

chat_router = APIRouter()


def get_repositories() -> DatabaseRepository[Message]:
    return get_message_repository()

