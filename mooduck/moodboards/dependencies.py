from typing import Annotated

from fastapi import Depends

from moodboards.models import Moodboard
from moodboards.services import get_moodboard
from users.models import User
from extra.dependencies import is_authenticated
from extra.exceptions import UnAuthorized


async def is_moodboard_author(
    user: Annotated[User, Depends(is_authenticated)],
    moodboard_id: int,
) -> tuple[User, Moodboard] | None:
    moodboard = await get_moodboard(moodboard_id)
    if not moodboard.author == user:
        raise UnAuthorized
    return user, moodboard
