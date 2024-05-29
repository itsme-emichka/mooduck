from datetime import datetime

from pydantic import BaseModel

from users.schemas import UserGet
from reactions.schemas import GetComment
from items.schemas import CreateItem, GetItem


class CreateMoodboard(BaseModel):
    name: str
    description: str | None = None
    cover: str | None = None
    is_private: bool = False
    existing_items: list[int] | None = None
    items: list[CreateItem] | None = None


# PATCH
class PatchMoodboard(BaseModel):
    name: str | None = None
    description: str | None = None
    cover: str | None = None
    is_private: bool | None = None


class GetMoodboard(BaseModel):
    id: int
    author: UserGet
    name: str
    description: str | None = None
    cover: str | None = None
    is_private: bool
    is_chaotic: bool
    created_at: datetime
    comments: list[GetComment] | None = None
    items: list[GetItem] | None = None


class ListMoodboard(BaseModel):
    id: int
    author: UserGet
    name: str
    description: str | None = None
    cover: str | None = None
    created_at: datetime
    is_private: bool
    is_chaotic: bool
