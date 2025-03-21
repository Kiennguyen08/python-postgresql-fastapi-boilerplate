from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.cores.database import Base


class ProjectSharing(Base):
    __tablename__ = "project_sharing"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    project_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
