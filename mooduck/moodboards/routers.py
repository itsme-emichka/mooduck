from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response
)

from users.models import User
from moodboards.models import Moodboard
from moodboards.schemas import (
    CreateMoodboard,
    GetMoodboard,
    ListMoodboard,
    AddItemsToMoodboard,
    PatchMoodboard

)
from moodboards.services import (
    bulk_create_items,
    get_moodboard_with_items as get_moodboard_with_items_db,
    add_existing_items_to_moodboard,
    get_all_moodboards,
    get_moodboard_items,
    get_chaotic,
    delete_item_from_moodboard as delete_item_from_moodboard_db,
    delete_moodboard as delete_moodboard_db,
    update_moodboard,
    get_user_fav_moodboards,
    add_moodboard_to_favorite as add_moodboard_to_favorite_db,
    remove_moodboard_from_fav
)
from moodboards.utils import get_moodboard_response
from moodboards.dependencies import is_moodboard_author
from extra.dependencies import is_authenticated
from extra.services import create_instance_by_kwargs


router = APIRouter()


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
        cover=data.cover,
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
    return get_moodboard_response(moodboard, items, user)


@router.get('/moodboard/{moodboard_id}')
async def retrieve_moodboard(moodboard_id: int) -> GetMoodboard:
    moodboard, items = await get_moodboard_with_items_db(moodboard_id)
    return get_moodboard_response(moodboard, items, moodboard.author)


@router.delete('/moodboard/{moodboard_id}')
async def delete_moodboard(
    moodboard_id: int,
    user_moodboard: Annotated[
        tuple[User, Moodboard],
        Depends(is_moodboard_author)
    ],
) -> None:
    user, moodboard = user_moodboard
    await delete_moodboard_db(moodboard)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/moodboard')
async def list_moodboard() -> list[ListMoodboard]:
    return await get_all_moodboards()


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
    await update_moodboard(moodboard, **data)
    return await retrieve_moodboard(moodboard_id)


# FAV
@router.get('/fav')
async def list_fav_moodboard(
    user: Annotated[User, Depends(is_authenticated)]
) -> list[GetMoodboard]:
    return await get_user_fav_moodboards(user)


@router.post('/moodboard/{moodboard_id}/fav')
async def add_moodboard_to_favorite(
    moodboard_id: int,
    user: Annotated[User, Depends(is_authenticated)],
) -> Response:
    await add_moodboard_to_favorite_db(user, moodboard_id)
    return Response(status_code=200)


@router.delete('/moodboard/{moodboard_id}/fav')
async def delete_moodboard_from_fav(
    moodboard_id: int,
    user: Annotated[User, Depends(is_authenticated)]
) -> Response:
    await remove_moodboard_from_fav(user, moodboard_id)


# ITEMS
@router.post('/moodboard/{moodboard_id}')
async def add_items_to_moodboard(
    moodboard_id: int,
    user_moodboard: Annotated[
        tuple[User, Moodboard],
        Depends(is_moodboard_author)
    ],
    data: AddItemsToMoodboard
) -> GetMoodboard:
    user, moodboard = user_moodboard
    items = []
    if data.items:
        items = await bulk_create_items(user, moodboard, data.items)
    if data.existing_items:
        items.extend(
            await add_existing_items_to_moodboard(
                data.existing_items,
                moodboard
            )
        )
    if not items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пустой запрос или такие айтемы уже на мудборде'
        )
    return get_moodboard_response(
        moodboard,
        await get_moodboard_items(moodboard),
        moodboard.author
    )


@router.delete('/moodboard/{moodboard_id}/{item_id}')
async def delete_item_from_moodboard(
    moodboard_id: int,
    item_id: int,
    user_moodboard: Annotated[
        tuple[User, Moodboard],
        Depends(is_moodboard_author)
    ],
) -> GetMoodboard:
    user, moodboard = user_moodboard
    await delete_item_from_moodboard_db(
        user=user,
        moodboard=moodboard,
        item_id=item_id,
    )
    return get_moodboard_response(
        moodboard,
        await get_moodboard_items(moodboard),
        moodboard.author
    )


# CHAOTIC
@router.get('/chaotic')
async def retrive_chaotic(
    user: Annotated[User, Depends(is_authenticated)]
) -> GetMoodboard:
    moodboard = await get_chaotic(user)
    return get_moodboard_response(
        moodboard=moodboard,
        items=await get_moodboard_items(moodboard),
        author=moodboard.author
    )


@router.post('/chaotic')
async def add_items_to_chaotic(
    user: Annotated[User, Depends(is_authenticated)],
    data: AddItemsToMoodboard
) -> GetMoodboard:
    moodboard = await get_chaotic(user)
    items = []
    if data.items:
        items = await bulk_create_items(user, moodboard, data.items)
    if data.existing_items:
        items.extend(
            await add_existing_items_to_moodboard(
                data.existing_items,
                moodboard
            )
        )
    if not items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Пустой запрос или такие айтемы уже на мудборде'
        )
    return get_moodboard_response(
        moodboard,
        await get_moodboard_items(moodboard),
        moodboard.author
    )


@router.delete('/chaotic/{item_id}')
async def delete_item_from_chaotic(
    user: Annotated[User, Depends(is_authenticated)],
    item_id: int,
) -> GetMoodboard:
    moodboard = await get_chaotic(user)
    await delete_item_from_moodboard_db(
        user=user,
        moodboard=moodboard,
        item_id=item_id,
    )
    return get_moodboard_response(
        moodboard,
        await get_moodboard_items(moodboard),
        moodboard.author
    )
