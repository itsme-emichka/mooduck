from pydantic import BaseModel

from users.schemas import UserGet


class Moodboard(BaseModel):
    id: int
    author: UserGet
    name: str
    description: str | None = None
    cover: str | None = None
    is_private: bool = False
    is_chaotic: bool = False

    class Config:
        from_attributes = True
