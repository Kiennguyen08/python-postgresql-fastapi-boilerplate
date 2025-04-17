from dataclasses import dataclass

from fastapi import WebSocket

from app.constants.enum import TimeZone


@dataclass
class SessionMetadata:
    websocket: WebSocket
    timezone: TimeZone
