from typing import Annotated

from fastapi import APIRouter, Depends

from users.models import User
from moodboards.models import Moodboard
from moodboards.schemas import (
    CreateMoodboard,
    GetMoodboard,
)
from moodboards.services import (
    bulk_create_items,
    get_moodboard as get_moodboard_db,
    add_existing_items_to_moodboard,
    get_all_moodboards
)
from moodboards.utils import get_moodboard_response
from extra.dependencies import is_authenticated
from extra.services import create_instance_by_kwargs


router = APIRouter()


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
    moodboard, items = await get_moodboard_db(id)
    return get_moodboard_response(moodboard, items, moodboard.author)


@router.get('/moodboard')
async def list_moodboard() -> list[GetMoodboard]:
    return await get_all_moodboards()
