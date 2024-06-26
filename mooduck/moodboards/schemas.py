from datetime import datetime
from typing import Annotated

from pydantic import BaseModel
from fastapi import Query

from config import BASE64_PATTERN
from users.schemas import UserGet
from reactions.schemas import GetComment
from items.schemas import CreateItem, GetItem
from extra.schemas import Pagination


class CreateMoodboard(BaseModel):
    name: str
    description: str | None = None
    cover: Annotated[str | None, Query(pattern=BASE64_PATTERN)] = None
    is_private: bool = False
    existing_items: list[int] | None = None
    items: list[CreateItem] | None = None


# PATCH
class PatchMoodboard(BaseModel):
    name: str | None = None
    description: str | None = None
    cover: Annotated[str | None, Query(pattern=BASE64_PATTERN)] = None
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
    likes: int = 0
    is_liked: bool = False
    is_in_favorite: bool = False
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
    likes: int = 0

    class Config:
        from_attributes = True


class PaginatedMoodboard(Pagination):
    items: list[ListMoodboard]


class GetChaotic(BaseModel):
    id: int
    author: UserGet
    name: str
    description: str | None = None
    cover: str | None = None
    is_private: bool
    is_chaotic: bool
    created_at: datetime
    items: list[GetItem] | None = None
