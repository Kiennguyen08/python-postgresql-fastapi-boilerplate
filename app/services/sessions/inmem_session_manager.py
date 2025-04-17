import logging

from app import config
from app.dto.session_metadata import SessionMetadata

logger = logging.getLogger(__name__)


class InMemorySessionManager:
    def __init__(self):
        self.active_sessions = {}
        self.max_clients = config.contraint.max_clients

    async def acquire(self, session_id: str, metadata: SessionMetadata):
        logger.info(f"Current number online sessions: {len(self.active_sessions)}")
        if len(self.active_sessions) >= self.max_clients:
            raise Exception("Max client reached")
        elif session_id in self.active_sessions:
            raise Exception(f"Session ID: {session_id} already connected.")
        self.active_sessions[session_id] = metadata

    async def release(self, session_id: str):
        if session_id not in self.active_sessions:
            raise Exception(f"No active session with id: {session_id}")
        del self.active_sessions[session_id]

    async def count(self, session_id: str):
        return len(self.active_sessions)

    async def get_session(self, session_id: str):
        if session_id not in self.active_sessions:
            raise Exception(f"No active session with id: {session_id}")
        metadata = self.active_sessions[session_id]
        return metadata
