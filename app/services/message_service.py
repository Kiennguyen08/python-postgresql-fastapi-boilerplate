import asyncio
from datetime import datetime

from app.dto.message import Message as MessageDTO
from app.models.message import Message
from app.repositories.database_repository import DatabaseRepository


class MessageService:
    def __init__(
        self,
        repository: DatabaseRepository[Message],
    ):
        self.repository = repository

    async def list_messages(
        self,
        client_id: str,
        page: int = 0,
        limit: int = 10,
    ):
        filter = [Message.client_id == client_id]
        order_by = Message.timestamp.desc()
        entities_task = self.repository.filter(
            *filter, skip=page, limit=limit, order_by=order_by
        )
        total_item_searched_task = self.repository.count(*filter)
        entities, total_item_searched = await asyncio.gather(
            entities_task, total_item_searched_task
        )
        # entities = await self.repository.filter(
        #     *filter, skip=page, limit=limit, order_by=order_by
        # )
        # total_item_searched = await self.repository.count(*filter)

        return entities, total_item_searched

    async def save_message(self, message: MessageDTO) -> Message:
        session = self.repository.session
        entity = message.to_model()
        session.add(entity)
        await session.flush()
        await session.commit()
        return entity

    async def update_message_status(
        self,
        message_id: int,
        status: str,
    ):
        session = self.repository.session
        query = [Message.id == message_id]
        entity = await self.repository.get(*query)

        if entity is None:
            raise ValueError(f"Message with ID {message_id} not found")

        entity.status = status
        entity.timestamp = datetime.now()

        session.add(entity)
        await session.commit()
