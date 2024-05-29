from fastapi import HTTPException
from tortoise.exceptions import IntegrityError

from reactions.models import Comment
from moodboards.models import Moodboard
from users.models import User


async def get_moodboard_comments(moodboard: Moodboard) -> list[Comment]:
    return await Comment.all(
    ).select_related(
        'moodboard'
    ).select_related(
        'author'
    ).select_related(
        'answering_to'
    ).filter(moodboard=moodboard)


async def get_comment(id: int) -> Comment:
    comment = await Comment.all(
    ).select_related(
        'author'
    ).select_related(
        'answering_to'
    ).get_or_none(id=id)
    if not comment:
        raise HTTPException(404)
    return comment


async def add_comment_to_moodboard(
    user: User,
    moodboard: Moodboard,
    text: str,
    answering_to: Comment | None = None,
) -> Moodboard:
    try:
        await Comment.create(
            author=user,
            answering_to=answering_to,
            moodboard=moodboard,
            text=text
        )
    except IntegrityError as ex:
        print(ex)
        raise HTTPException(400, 'wrong data')
    return moodboard
