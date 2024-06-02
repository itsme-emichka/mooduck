from typing import Annotated

from fastapi import Depends

from users.models import User
from items.models import Item
from items.services import get_item
from extra.dependencies import is_authenticated
from extra.exceptions import UnAuthorized


async def is_item_author(
    user: Annotated[User, Depends(is_authenticated)],
    item_id: int,
) -> tuple[User, Item]:
    item = await get_item(item_id)
    if not item.author == user:
        raise UnAuthorized
    return user, item
