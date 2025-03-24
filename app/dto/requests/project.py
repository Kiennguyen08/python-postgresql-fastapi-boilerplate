from pydantic import BaseModel, constr


class CreateProjectRequest(BaseModel):
    name: constr(max_length=50)
    description: constr(max_length=200)


class CreateProjectInternalRequest(CreateProjectRequest):
    user_id: str
