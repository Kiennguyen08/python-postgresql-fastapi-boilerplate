import asyncio
import logging
import random
from datetime import datetime

import pytz
from fastapi import WebSocket, WebSocketDisconnect

from app.config import config
from app.constants.enum import MessageType, TimeZone
from app.dto.session_metadata import SessionMetadata
from app.services.sessions.session_manager import SessionManager

logger = logging.getLogger(__name__)


class ConnectionManagerService:
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.message_count = 0
        self.max_clients = config.contraint.max_clients
        self.max_messages = config.contraint.max_messages

    async def connect(self, websocket: WebSocket, client_id: str):
        try:
            timezone = random.choice(
                [
                    TimeZone.EUROPE_LONDON,
                    TimeZone.AMERICA_NEW_YORK,
                    TimeZone.ASIA_HO_CHI_MINH,
                    TimeZone.ASIA_TOKYO,
                ]
            )
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

    async def process_message(self, client_id: str, message: dict):
        if self.message_count >= self.max_messages:
            return

        client = await self.session_manager.get_session(session_id=client_id)
        tz = pytz.timezone(client.timezone.value)
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

        if valid:
            self.message_count += 1

            # Simulate processing delay
            delay = random.uniform(
                0 if msg_type == MessageType.TEXT else 1 if msg_type == MessageType.VOICE else 2,
                1 if msg_type == MessageType.TEXT else 2 if msg_type == MessageType.VOICE else 3,
            )
            await asyncio.sleep(delay)

            # Generate replies
            replies = []
            if msg_type == MessageType.TEXT:
                replies.append(
                    {"type": MessageType.TEXT, "content": "GPT: Message received!"}
                )
            if msg_type == MessageType.VOICE:
                replies.append({"type": MessageType.VOICE, "content": "12345"})
            elif msg_type == MessageType.VIDEO:
                replies.extend(
                    [
                        {"type": MessageType.VIDEO, "content": "12345"},
                    ]
                )

            # Send replies
            try:
                for reply in replies:
                    await client.websocket.send_json(reply)
                    # TODO: Update DB status to success
            except WebSocketDisconnect:
                # TODO: update message in DB with status = 'failed and date = datetime.now().isoformat()
                pass
        else:
            # TODO: update message in DB with status = 'failed and date = datetime.now().isoformat()
            pass
