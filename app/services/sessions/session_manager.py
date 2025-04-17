from app.dto.session_metadata import SessionMetadata


class SessionManager:
    def __init__(self):
        pass

    async def acquire(self, session_id: str, metadata: SessionMetadata):
        raise NotImplementedError()

    async def release(self, session_id: str):
        raise NotImplementedError()

    async def count(self, session_id: str):
        raise NotImplementedError()

    async def get_session(self, session_id: str) -> SessionMetadata:
        raise NotImplementedError()
