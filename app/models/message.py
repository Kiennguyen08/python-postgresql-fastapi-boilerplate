from sqlalchemy import Column, DateTime, Integer, Text

from app.cores.database import Base


class Message(Base):
    """Projects database model."""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
