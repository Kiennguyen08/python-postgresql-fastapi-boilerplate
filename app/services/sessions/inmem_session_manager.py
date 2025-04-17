from app import config
from app.cores.errors import BadRequestException
from app.dto.session_metadata import SessionMetadata


class InMemorySessionManager:
    def __init__(self):
        self.active_sessions = {}
        self.max_clients = config.contraint.max_clients

    async def acquire(self, session_id: str, metadata: SessionMetadata):
        if len(self.active_sessions) >= self.max_clients:
            raise Exception("Max client reached")
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
        return self.active_sessions[session_id]
