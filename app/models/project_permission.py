from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.cores.database import Base


class ProjectPermission(Base):
    __tablename__ = "project_permission"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    project_id = Column(String(36), nullable=False)
    permission_type = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )
    deleted_at = Column(DateTime, nullable=True)
