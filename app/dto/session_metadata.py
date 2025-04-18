from dataclasses import asdict, dataclass
from typing import Any, Dict

from fastapi import WebSocket

from app.constants.enum import TimeZone


@dataclass
class SessionMetadata:
    websocket: WebSocket
    timezone: TimeZone

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionMetadata":
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
