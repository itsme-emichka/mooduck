from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, field_validator
from fastapi import Query

from items.models import ITEM_TYPES
from users.schemas import UserGet
from config import BASE64_PATTERN
from extra.schemas import Pagination


class CreateItem(BaseModel):
    name: str
    description: str | None = None
    item_type: str
    link: str | None = None
    is_private: bool = False
    media: Annotated[
        list[str] | None,
        list[Query(pattern=BASE64_PATTERN)]
    ] = None

    @field_validator('item_type')
    @classmethod
    def item_type_validator(cls, value: str):
        if value not in ITEM_TYPES.keys():
            raise ValueError(
                f'Item type {value} not available '
                f'Types available: {ITEM_TYPES.keys()}'
            )
        return value


class PatchItem(BaseModel):
    name: str | None = None
    description: str | None = None
    item_type: str | None = None
    link: str | None = None
    is_private: bool | None = None
    media: list[str] | None = None

    @field_validator('item_type')
    @classmethod
    def item_type_validator(cls, value: str):
        if value not in ITEM_TYPES.keys():
            raise ValueError(
                f'Item type {value} not available '
                f'Types available: {ITEM_TYPES.keys()}'
            )
        return value


class GetItem(BaseModel):
    id: int
    author: UserGet
    name: str
    description: str | None = None
    item_type: str
    link: str | None = None
    is_private: bool = False
    media: list[str] | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class AddItemsToMoodboard(BaseModel):
    items: list[CreateItem] | None = None
    existing_items: list[int] | None = None


class PaginatedItem(Pagination):
    items: list[GetItem]
