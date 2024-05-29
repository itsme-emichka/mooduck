from typing import Annotated

from fastapi import Depends, HTTPException, status

from users.models import User
from items.models import Item
from items.services import get_item
from extra.dependencies import is_authenticated


async def is_item_author(
    user: Annotated[User, Depends(is_authenticated)],
    item_id: int,
) -> tuple[User, Item]:
    item = await get_item(item_id)
    if not item.author == user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='У вас недостаточно прав для доступа к данной записи'
        )
    return user, item
