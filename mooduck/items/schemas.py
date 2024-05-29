from datetime import datetime

from pydantic import BaseModel, field_validator

from items.models import ITEM_TYPES
from users.schemas import UserGet


class CreateItem(BaseModel):
    name: str
    description: str | None = None
    item_type: str
    link: str | None = None
    media: list[str] = ['']

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
    media: list[str] | None = None
    created_at: datetime

    class Config:
        from_attributes = True


class AddItemsToMoodboard(BaseModel):
    items: list[CreateItem] | None = None
    existing_items: list[int] | None = None
