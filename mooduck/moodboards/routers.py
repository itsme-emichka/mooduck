from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from users.models import User
from moodboards.models import Moodboard
from moodboards.schemas import (
    CreateMoodboard,
    GetMoodboard,
    ListMoodboard,
    AddItemsToMoodboard
)
from moodboards.services import (
    bulk_create_items,
    get_moodboard_with_items as get_moodboard_with_items_db,
    add_existing_items_to_moodboard,
    get_all_moodboards,
    get_moodboard,
    get_moodboard_items,
    get_chaotic,
    delete_item_from_moodboard as delete_item_from_moodboard_db
)
from moodboards.utils import get_moodboard_response
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


@router.get('/moodboard/{id}')
async def retrieve_moodboard(id: int) -> GetMoodboard:
    moodboard, items = await get_moodboard_with_items_db(id)
    return get_moodboard_response(moodboard, items, moodboard.author)


@router.post('/moodboard/{id}')
async def add_items_to_moodboard(
    id: int,
    user: Annotated[User, Depends(is_authenticated)],
    data: AddItemsToMoodboard
) -> GetMoodboard:
    moodboard = await get_moodboard(id)
    if not user == moodboard.author:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не ваш мудборд'
        )
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


@router.delete('/moodboard/{id}/{item_id}')
async def delete_item_from_moodboard(
    id: int,
    item_id: int,
    user: Annotated[User, Depends(is_authenticated)]
) -> GetMoodboard:
    moodboard = await get_moodboard(id)
    if not user == moodboard.author:
        raise HTTPException(
            status_code=401)
    await delete_item_from_moodboard_db(moodboard, item_id)
    return get_moodboard_response(
        moodboard,
        await get_moodboard_items(moodboard),
        moodboard.author
    )


@router.get('/moodboard')
async def list_moodboard() -> list[ListMoodboard]:
    return await get_all_moodboards()


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
    await delete_item_from_moodboard_db(moodboard, item_id)
    return get_moodboard_response(
        moodboard,
        await get_moodboard_items(moodboard),
        moodboard.author
    )
