from pydantic import BaseModel


class Pagination(BaseModel):
    page: int = 1
    limit: int = 30
    prev_page: str | None
    next_page: str | None
    amount: int
    items: list[BaseModel] = []
