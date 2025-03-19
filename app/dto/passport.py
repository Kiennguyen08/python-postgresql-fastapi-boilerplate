from pydantic import BaseModel


class UserData(BaseModel):
    id: str
    fullname: str
    is_blocked: bool


class PassportResponse(BaseModel):
    data: UserData
