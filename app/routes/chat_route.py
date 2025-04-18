from typing import List, Optional

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect

from app.dto.message import ListMessageResponseData
from app.dto.message import Message as MessageDTO
from app.dto.message import MessageResponse
from app.models.message import Message
from app.repositories.database_repository import DatabaseRepository
from app.routes.dependencies.db_repository import get_message_repository
from app.services.connection_manager_service import ConnectionManagerService
from app.services.message_service import MessageService
from app.services.sessions.inmem_session_manager import InMemorySessionManager

chat_router = APIRouter()
session_manager = InMemorySessionManager()
connection_manager = ConnectionManagerService(session_manager=session_manager)


@chat_router.websocket("/chat/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str,
    timezone: str,
    repository: DatabaseRepository[Message] = Depends(get_message_repository),
):
    message_service = MessageService(repository=repository)
    await websocket.accept()
    connected = await connection_manager.connect(websocket, client_id, timezone)
    if not connected:
        return

    try:
        while True:
            data = await websocket.receive_json()
            await connection_manager.process_message(
                message_service, client_id, data, timezone
            )
    except WebSocketDisconnect:
        await connection_manager.disconnect(client_id)


@chat_router.get("/chat_history")
async def get_chat_history(
    client_id: str,
    page: Optional[int] = Query(
        0, ge=0, description="Number of records to skip for pagination"
    ),
    limit: Optional[int] = Query(
        10, le=100, description="Number of records to return per page"
    ),
    repository: DatabaseRepository[Message] = Depends(get_message_repository),
):
    message_service = MessageService(repository=repository)
    messages, total = await message_service.list_messages(
        client_id=client_id, page=page, limit=limit
    )
    items: List[MessageDTO] = []
    for entity in messages:
        message = MessageDTO.model_validate(entity)
        items.append(message)

    return MessageResponse(
        message="Get messages successfully",
        data=ListMessageResponseData(total_item=total, items=items),
    )
