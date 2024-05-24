from typing import Annotated

from pydantic import BaseModel, EmailStr
from fastapi import Query

from config import SLUG_PATTERN, EMAIL_PATTERN


class UserGet(BaseModel):
    id: int
    username: str
    email: EmailStr
    name: str | None = None
    role: str = 'user'


class UserCreate(BaseModel):
    username: Annotated[str, Query(pattern=SLUG_PATTERN)]
    email: Annotated[str, Query(pattern=EMAIL_PATTERN)]
    password: str
    name: str | None = None
