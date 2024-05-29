from datetime import datetime

from pydantic import BaseModel

from users.schemas import UserGet


class CreateComment(BaseModel):
    text: str


class GetComment(BaseModel):
    id: int
    author: UserGet
    answering_to: int | None = None
    text: str
    created_at: datetime

    class Config:
        from_attributes = True
