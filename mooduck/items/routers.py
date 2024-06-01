from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response

from users.models import User
from extra.dependencies import is_authenticated, pagination
from extra.schemas import Pagination
from items.models import Item
from items.schemas import AddItemsToMoodboard, PatchItem, GetItem
from items.services import (
    bulk_create_items,
    add_existing_items_to_moodboard,
    get_moodboard_items,
    delete_item_from_moodboard as delete_item_from_moodboard_db,
    update_item,
    get_item_check_authorization,
    get_random_item,
    get_all_items
)
from items.dependencies import is_item_author
from items.utils import get_item_response, get_item_list_response
from moodboards.schemas import GetMoodboard
from moodboards.services import (
    get_chaotic,
    get_moodboard_check_authorization
)
from moodboards.utils import get_moodboard_response
from moodboards.dependencies import is_moodboard_author
from moodboards.models import Moodboard
from reactions.services import get_moodboard_comments


router = APIRouter()


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
        await get_moodboard_comments(moodboard)
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
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/moodboard/{moodboard_id}/item')
async def add_items_to_moodboard(
    user_moodboard: Annotated[
        tuple[User, Moodboard],
        Depends(is_moodboard_author)
    ],
    data: AddItemsToMoodboard
) -> list[GetItem]:
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
    return get_item_list_response(items)


@router.get('/moodboard/{moodboard_id}/item')
async def list_moodboard_items(
    moodboard_id: int,
    user: Annotated[User, Depends(is_authenticated)]
) -> list[GetItem]:
    moodboard = await get_moodboard_check_authorization(moodboard_id, user)
    return get_item_list_response(await get_moodboard_items(moodboard))


@router.delete('/moodboard/{moodboard_id}/item/{item_id}')
async def delete_item_from_moodboard(
    item_id: int,
    user_moodboard: Annotated[
        tuple[User, Moodboard],
        Depends(is_moodboard_author)
    ],
):
    user, moodboard = user_moodboard
    await delete_item_from_moodboard_db(
        user=user,
        moodboard=moodboard,
        item_id=item_id,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/item/{item_id}')
async def retrieve_moodboard_item(
    user: Annotated[User, Depends(is_authenticated)],
    item_id: int,
) -> GetItem:
    return get_item_response(
        await get_item_check_authorization(user, item_id)
    )


@router.patch('/item/{item_id}')
async def patch_item(
    user_item: Annotated[
        tuple[User, Item],
        Depends(is_item_author)
    ],
    data: PatchItem
) -> GetItem:
    user, item = user_item
    data = data.model_dump(exclude_none=True)
    updated_item = await update_item(item, data)
    return get_item_response(updated_item)


@router.get('/item')
async def list_items(
    user: Annotated[User, Depends(is_authenticated)],
    paginator=Depends(pagination),
    search: str | None = None,
    item_type: str | None = None
) -> Pagination:
    return await paginator(
        get_all_items(search, item_type),
        GetItem,
        get_item_response
    )


@router.get('/random/item')
async def retrieve_random_item(
    user: Annotated[User, Depends(is_authenticated)],
    item_type: str | None = None
) -> GetItem:
    return get_item_response(await get_random_item(item_type))
