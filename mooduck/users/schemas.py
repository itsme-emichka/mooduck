from typing import Annotated

from pydantic import BaseModel, EmailStr
from fastapi import Query

from config import SLUG_PATTERN
from extra.schemas import Pagination


class UserGet(BaseModel):
    id: int
    username: str
    email: EmailStr
    name: str | None = None
    role: str = 'user'
    bio: str | None = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: Annotated[str, Query(pattern=SLUG_PATTERN)]
    email: EmailStr
    password: str
    name: str | None = None
    bio: str | None = None


class PaginatedUser(Pagination):
    items: list[UserGet]
