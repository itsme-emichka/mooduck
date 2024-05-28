from typing import Annotated

from fastapi import Depends, HTTPException, status

from moodboards.models import Moodboard, Item
from moodboards.services import get_moodboard, get_item
from users.models import User
from extra.dependencies import is_authenticated


async def is_moodboard_author(
    user: Annotated[User, Depends(is_authenticated)],
    moodboard_id: int,
) -> tuple[User, Moodboard] | None:
    moodboard = await get_moodboard(moodboard_id)
    if not moodboard.author == user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='У вас недостаточно прав для доступа к данной записи'
        )
    return user, moodboard


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
