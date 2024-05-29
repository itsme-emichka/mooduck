from typing import Annotated

from fastapi import Depends, HTTPException

from reactions.models import Comment
from reactions.services import get_comment
from extra.dependencies import is_authenticated
from users.models import User


async def is_comment_author(
    user: Annotated[User, Depends(is_authenticated)],
    comment_id: int
) -> list[User, Comment]:
    comment = await get_comment(comment_id)
    if not comment.author == user:
        raise HTTPException(401)
    return user, comment
