from datetime import datetime
from typing import List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.dto.response_dto import BaseResponseData


class Project(BaseModel):
    id: Union[str, UUID]
    name: str
    description: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class ListProjectResponseData(BaseModel):
    total_item: int
    items: Optional[List[Project]]


class ProjectResponse(BaseResponseData):
    data: Union[ListProjectResponseData, Project]
