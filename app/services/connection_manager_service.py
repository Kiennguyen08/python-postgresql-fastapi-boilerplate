import asyncio
import logging
import random
import time
from datetime import datetime

import pytz
from fastapi import WebSocket, WebSocketDisconnect

from app.config import config
from app.constants.enum import MessageStatus, MessageType
from app.dto.message import Message
from app.dto.session_metadata import SessionMetadata
from app.services.message_service import MessageService
from app.services.sessions.session_manager import SessionManager

logger = logging.getLogger(__name__)


class ConnectionManagerService:
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.max_clients = config.contraint.max_clients
        self.max_messages = config.contraint.max_messages
        self.message_queue = asyncio.Queue(maxsize=self.max_messages)

    async def connect(self, websocket: WebSocket, client_id: str, timezone: str):
        try:
            session_metadata: SessionMetadata = SessionMetadata(
                websocket=websocket,
                timezone=timezone,
            )

            await self.session_manager.acquire(
                session_id=client_id, metadata=session_metadata
            )
            return True
        except Exception as exc:
            await websocket.close(code=1008, reason=str(exc))
            return False

    async def disconnect(self, client_id: str):
        try:
            await self.session_manager.release(session_id=client_id)
        except Exception as exc:
            logger.error(
                f"Exception in disconnecting client: {client_id}", exc_info=exc
            )

    async def process_message(
        self,
        message_service: MessageService,
        client_id: str,
        message: dict,
        timezone: str,
    ):
        client_time = self.get_client_time(timezone)
        client = await self.session_manager.get_session(session_id=client_id)
        if self.message_queue.full():
            await client.websocket.send_json(
                {
                    "type": MessageType.TEXT,
                    "content": "Reached max messages can be processed!",
                }
            )
            return

        tz = pytz.timezone(client.timezone)
        now = datetime.now(tz)
        msg_type = message["type"]

        # Time validation
        valid = False
        if msg_type == MessageType.TEXT and 5 <= now.hour < 24:
            valid = True
        elif msg_type == MessageType.VOICE and 8 <= now.hour < 12:
            valid = True
        elif msg_type == MessageType.VIDEO and 20 <= now.hour < 24:
            valid = True

        # Save to database
        # TODO: insert message in DB with client_id, msg_type, content, 'status' = pending, and datetime.now().isoformat()
        message_dto = Message(
            client_id=client_id,
            type=msg_type,
            content=message.get("content"),
            status=MessageStatus.PENDING,
            timestamp=datetime.now(),
        )
        entity = await message_service.save_message(message=message_dto)

        if valid:
            await self.message_queue.put(1)

            # Simulate processing delay
            replies = []
            if msg_type == MessageType.TEXT:
                if 5 <= client_time.hour < 24:
                    delay = random.uniform(0, 1)
                    replies.append(
                        {"type": MessageType.TEXT, "content": "GPT: Message received!"}
                    )
                else:
                    replies.append(
                        {
                            "type": MessageType.TEXT,
                            "content": "Message rejected: Outside allowed time for text chat.",
                        }
                    )
            if msg_type == MessageType.VOICE:
                if 8 <= client_time.hour < 12:
                    delay = random.uniform(1, 2)
                    replies.append({"type": MessageType.VOICE, "content": "12345"})
                else:
                    replies.append(
                        {
                            "type": MessageType.TEXT,
                            "content": "Message rejected: Outside allowed time for voice chat.",
                        }
                    )
            elif msg_type == MessageType.VIDEO:
                if 20 <= client_time.hour < 24:
                    delay = random.uniform(2, 3)
                    replies.append(
                        {"type": MessageType.VIDEO, "content": "12345"},
                    )
                else:
                    replies.append(
                        {
                            "type": MessageType.TEXT,
                            "content": "Message rejected: Outside allowed time for video chat.",
                        }
                    )
            await asyncio.sleep(delay)

            # Send replies
            try:
                for reply in replies:
                    await client.websocket.send_json(reply)
                    # TODO: Update DB status to success
                    await message_service.update_message_status(
                        message_id=entity.id, status=MessageStatus.SUCCESS
                    )
            except WebSocketDisconnect:
                # TODO: update message in DB with status = 'failed and date = datetime.now().isoformat()
                await message_service.update_message_status(
                    message_id=entity.id, status=MessageStatus.FAIL
                )
                pass
        else:
            # TODO: update message in DB with status = 'failed and date = datetime.now().isoformat()
            await message_service.update_message_status(
                message_id=entity.id, status=MessageStatus.FAIL
            )
            pass

        await self.message_queue.get()

    def get_client_time(self, timezone):
        return datetime.now(pytz.timezone(timezone))
