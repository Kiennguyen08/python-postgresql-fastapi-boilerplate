from typing import List, Optional, Tuple

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.models.message import Message
from app.repositories.database_repository import DatabaseRepository
from app.routes.dependencies.db_repository import get_message_repository
from app.services.connection_manager_service import ConnectionManagerService
from app.services.sessions.inmem_session_manager import InMemorySessionManager

chat_router = APIRouter()
session_manager = InMemorySessionManager()
connection_manager = ConnectionManagerService(session_manager=session_manager)


def get_repositories() -> DatabaseRepository[Message]:
    return get_message_repository()


@chat_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    connected = await connection_manager.connect(websocket, client_id)
    if not connected:
        return

    try:
        while True:
            data = await websocket.receive_json()
            await connection_manager.process_message(client_id, data)
    except WebSocketDisconnect:
        await connection_manager.disconnect[client_id]
