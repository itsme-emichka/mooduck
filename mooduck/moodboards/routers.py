from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
    Query,
)

from users.models import User
from moodboards.models import Moodboard
from moodboards.schemas import (
    CreateMoodboard,
    GetMoodboard,
    PatchMoodboard,
    ListMoodboard
)
from moodboards.services import (
    get_moodboard_with_items_and_comments,
    get_moodboard_items,
    get_chaotic,
    delete_moodboard as delete_moodboard_db,
    update_moodboard,
    get_user_fav_moodboards,
    add_moodboard_to_favorite as add_moodboard_to_favorite_db,
    remove_moodboard_from_fav,
    get_user_moodboards,
    get_user_subs_moodboards,
    get_random_moodboard,
    get_moodboards
)
from moodboards.utils import get_moodboard_response
from moodboards.dependencies import is_moodboard_author
from extra.dependencies import is_authenticated, pagination
from extra.services import create_instance_by_kwargs, get_instance_or_404
from extra.utils import save_image_from_base64
from extra.schemas import Pagination
from reactions.routers import router as reactions_router
from reactions.services import get_moodboard_comments
from items.routers import router as items_router
from items.services import bulk_create_items, add_existing_items_to_moodboard


router = APIRouter()
router.include_router(reactions_router)
router.include_router(items_router)


# MOODBOARD
@router.post('/moodboard')
async def create_moodboard(
    user: Annotated[User, Depends(is_authenticated)],
    data: CreateMoodboard
) -> GetMoodboard:
    moodboard: Moodboard = await create_instance_by_kwargs(
        Moodboard,
        author=user,
        name=data.name,
        description=data.description,
        cover=save_image_from_base64(data.cover),
        is_private=data.is_private,
    )
    items = []
    if data.items:
        items: list = await bulk_create_items(user, moodboard, data.items)
    if data.existing_items:
        existing_items = await add_existing_items_to_moodboard(
            data.existing_items,
            moodboard
        )
        items.extend(existing_items)
    return get_moodboard_response(moodboard, items, [], False)


@router.get('/moodboard/{moodboard_id}')
async def retrieve_moodboard(
    moodboard_id: int,
    user: Annotated[User, Depends(is_authenticated)]
) -> GetMoodboard:
    moodboard, items, comments = await get_moodboard_with_items_and_comments(
        moodboard_id,
        user
    )
    return get_moodboard_response(
        moodboard,
        items,
        comments,
        await user.is_moodboard_liked(moodboard_id)
    )


@router.delete('/moodboard/{moodboard_id}')
async def delete_moodboard(
    moodboard_id: int,
    user_moodboard: Annotated[
        tuple[User, Moodboard],
        Depends(is_moodboard_author)
    ],
):
    user, moodboard = user_moodboard
    await delete_moodboard_db(moodboard)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch('/moodboard/{moodboard_id}')
async def patch_moodboard(
    moodboard_id: int,
    user_moodboard: Annotated[
        tuple[User, Moodboard],
        Depends(is_moodboard_author)
    ],
    data: PatchMoodboard,
):
    user, moodboard = user_moodboard
    data = data.model_dump(exclude_none=True)
    moodboard = await update_moodboard(moodboard, data)
    return get_moodboard_response(
        moodboard,
        await get_moodboard_items(moodboard),
        await get_moodboard_comments(moodboard),
        await user.is_moodboard_liked(moodboard_id)
    )


@router.get('/random_moodboard')
async def retrieve_random_moodboard(
    user: Annotated[User, Depends(is_authenticated)],
) -> GetMoodboard:
    moodboard = await get_random_moodboard()
    return get_moodboard_response(
        moodboard,
        await get_moodboard_items(moodboard),
        await get_moodboard_comments(moodboard),
        await user.is_moodboard_liked(moodboard.id)
    )


@router.get('/moodboard')
async def list_moodboards(
    user: Annotated[User, Depends(is_authenticated)],
    paginator=Depends(pagination),
    search: str | None = None,
    period_from: int = 30,
    period_to: int = 0,
    sort: Annotated[
        str, Query(pattern=r'^(created_at|likes)$')
    ] = 'created_at',
) -> Pagination:
    queryset = get_moodboards(
        search=search,
        sort=sort,
        period_from=period_from,
        period_to=period_to
    )
    return await paginator(queryset, ListMoodboard)


@router.get('/user/me/moodboard')
async def retrieve_self_moodboards(
    user: Annotated[User, Depends(is_authenticated)],
    paginator=Depends(pagination)
) -> Pagination:
    return await paginator(get_user_moodboards(user, True), ListMoodboard)


@router.get('/user/{user_id}/moodboard')
async def list_user_moodboards(
    user_id: int,
    user: Annotated[User, Depends(is_authenticated)],
    paginator=Depends(pagination)
) -> Pagination:
    return await paginator(
        get_user_moodboards(await get_instance_or_404(User, id=user_id)),
        ListMoodboard
    )


# FAV
@router.get('/fav')
async def list_fav_moodboard(
    user: Annotated[User, Depends(is_authenticated)],
    paginator=Depends(pagination)
) -> Pagination:
    return await paginator(get_user_fav_moodboards(user), ListMoodboard)


@router.post('/moodboard/{moodboard_id}/fav')
async def add_moodboard_to_favorite(
    moodboard_id: int,
    user: Annotated[User, Depends(is_authenticated)],
):
    await add_moodboard_to_favorite_db(user, moodboard_id)


@router.delete('/moodboard/{moodboard_id}/fav')
async def delete_moodboard_from_fav(
    moodboard_id: int,
    user: Annotated[User, Depends(is_authenticated)]
):
    await remove_moodboard_from_fav(user, moodboard_id)


@router.get('/sub/moodboard')
async def get_subs_moodboards(
    user: Annotated[User, Depends(is_authenticated)],
    paginator=Depends(pagination)
) -> Pagination:
    return await paginator(await get_user_subs_moodboards(user), ListMoodboard)


# CHAOTIC
@router.get('/chaotic')
async def retrive_chaotic(
    user: Annotated[User, Depends(is_authenticated)]
) -> GetMoodboard:
    moodboard = await get_chaotic(user)
    return get_moodboard_response(
        moodboard,
        await get_moodboard_items(moodboard),
        await get_moodboard_comments(moodboard),
        False
    )
