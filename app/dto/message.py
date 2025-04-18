from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict

from app.dto.response_dto import BaseResponseData
from app.models.message import Message as MessageModel


class Message(BaseModel):
    id: Optional[int] = None
    client_id: str
    type: str
    content: str
    status: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

    def to_model(self):
        message_model = MessageModel(
            id=self.id,
            client_id=self.client_id,
            type=self.type,
            content=self.content,
            status=self.status,
            timestamp=self.timestamp,
        )
        return message_model


class ListMessageResponseData(BaseModel):
    total_item: int
    items: Optional[List[Message]]


class MessageResponse(BaseResponseData):
    data: Union[ListMessageResponseData, Message]
