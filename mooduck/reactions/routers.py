from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from users.models import User
from moodboards.services import (
    get_moodboard,
)
from reactions.schemas import CreateComment, GetComment
from reactions.services import (
    add_comment_to_moodboard,
    get_moodboard_comments,
    get_comment,
    update_comment,
    delete_comment as delete_comment_db,
    like_moodboard as like_moodboard_db,
    dislike_moodboard as dislike_moodboard_db
)
from reactions.utils import get_comment_list_response, get_comment_response
from reactions.models import Comment
from reactions.dependencies import is_comment_author
from extra.dependencies import is_authenticated


router = APIRouter()


@router.post('/moodboard/{moodboard_id}/comment')
async def leave_comment_to_moodboard(
    user: Annotated[User, Depends(is_authenticated)],
    moodboard_id: int,
    data: CreateComment
) -> list[GetComment]:
    moodboard = await get_moodboard(moodboard_id)
    await add_comment_to_moodboard(
        user=user,
        moodboard=moodboard,
        text=data.text
    )
    return get_comment_list_response(await get_moodboard_comments(moodboard))


@router.get('/moodboard/{moodboard_id}/comment')
async def list_of_moodboard_comments(
    user: Annotated[User, Depends(is_authenticated)],
    moodboard_id: int,
) -> list[GetComment]:
    moodboard = await get_moodboard(moodboard_id)
    return get_comment_list_response(await get_moodboard_comments(moodboard))


@router.get('/moodboard/{moodboard_id}/comment/{comment_id}')
async def retrieve_comment(
    user: Annotated[User, Depends(is_authenticated)],
    moodboard_id: int,
    comment_id: int,
) -> GetComment:
    comment = await get_comment(id=comment_id)

    return get_comment_response(comment)


@router.patch('/moodboard/{moodboard_id}/comment/{comment_id}')
async def edit_comment(
    user_comment: Annotated[list[User, Comment], Depends(is_comment_author)],
    data: CreateComment
) -> GetComment:
    user, comment = user_comment
    comment = await update_comment(comment, data.text)
    return get_comment_response(comment)


@router.delete('/moodboard/{moodboard_id}/comment/{comment_id}')
async def delete_comment(
    user_comment: Annotated[list[User, Comment], Depends(is_comment_author)],
):
    user, comment = user_comment
    await delete_comment_db(comment)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/moodboard/{moodboard_id}/comment/{comment_id}')
async def answer_to_another_comment(
    user: Annotated[User, Depends(is_authenticated)],
    moodboard_id: int,
    comment_id: int,
    data: CreateComment,
) -> list[GetComment]:
    moodboard = await get_moodboard(moodboard_id)
    comment = await get_comment(id=comment_id)

    await add_comment_to_moodboard(
        user=user,
        moodboard=moodboard,
        text=data.text,
        answering_to=comment
    )
    return get_comment_list_response(await get_moodboard_comments(moodboard))


@router.post('/moodboard/{moodboard_id}/like')
async def like_moodboard(
    moodboard_id: int,
    user: Annotated[User, Depends(is_authenticated)],
):
    await like_moodboard_db(user, moodboard_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete('/moodboard/{moodboard_id}/like')
async def dislike_moodboard(
    moodboard_id: int,
    user: Annotated[User, Depends(is_authenticated)]
):
    await dislike_moodboard_db(user, moodboard_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
