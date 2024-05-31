from fastapi import HTTPException
from tortoise.exceptions import IntegrityError

from reactions.models import Comment, Like
from moodboards.models import Moodboard
from users.models import User
from extra.services import get_instance_or_404


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


async def update_comment(comment: Comment, text: str) -> Comment:
    try:
        comment.update_from_dict({'text': text})
        await comment.save()
        return comment
    except IntegrityError as ex:
        print(ex)
        raise HTTPException(400)


async def delete_comment(comment: Comment) -> None:
    await comment.delete()


async def like_moodboard(user: User, moodboard_id: int):
    moodboard: Moodboard = await get_instance_or_404(
        Moodboard,
        id=moodboard_id,
    )
    like, is_created = await Like.get_or_create(
        author=user, moodboard=moodboard)
    if not is_created:
        raise HTTPException(400, 'already exists')
    await moodboard.add_like()


async def dislike_moodboard(user: User, moodboard_id: int):
    moodboard: Moodboard = await get_instance_or_404(
        Moodboard,
        id=moodboard_id,
    )
    like = await Like.get_or_none(author=user, moodboard=moodboard)
    if not like:
        raise HTTPException(404)
    await moodboard.remove_like()
    await like.delete()
