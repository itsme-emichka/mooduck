from datetime import datetime

from pydantic import BaseModel, field_validator

from users.schemas import UserGet
from moodboards.models import MOODBOARD_TYPES


# POST
class CreateItem(BaseModel):
    name: str
    description: str | None = None
    item_type: str
    link: str | None = None
    media: list[str] = ['']

    @field_validator('item_type')
    @classmethod
    def item_type_validator(cls, value: str):
        if value not in MOODBOARD_TYPES.keys():
            raise ValueError(
                f'Item type {value} not available '
                f'Types available: {MOODBOARD_TYPES.keys()}'
            )
        return value


class CreateMoodboard(BaseModel):
    name: str
    description: str | None = None
    cover: str | None = None
    is_private: bool = False
    existing_items: list[int] | None = None
    items: list[CreateItem] | None = None


# GET
class GetItem(BaseModel):
    id: int
    author: UserGet
    name: str
    description: str | None = None
    item_type: str
    link: str | None = None
    media: list[str] | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class GetMoodboard(BaseModel):
    id: int
    author: UserGet
    name: str
    description: str | None = None
    cover: str | None = None
    is_private: bool
    is_chaotic: bool
    created_at: datetime
    items: list[GetItem] | None = None


class ListMoodboard(BaseModel):
    id: int
    author: UserGet
    name: str
    description: str | None = None
    cover: str | None = None
    created_at: datetime