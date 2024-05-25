from fastapi import HTTPException
from users.models import User
from users.schemas import UserGet
from moodboards.models import (
    Moodboard,
    Item,
    ItemMoodboard,
)
from moodboards.schemas import CreateItem, GetItem


async def add_existing_items_to_moodboard(
    id_list: list[int],
    moodboard: Moodboard
) -> list[GetItem]:
    items = items = await Item.filter(id__in=id_list).select_related('author')
    await ItemMoodboard.bulk_create(
        [ItemMoodboard(
            item=item, moodboard=moodboard
            ) for item in items])
    return [
        GetItem(
            id=item.id,
            author=UserGet.model_validate(item.author),
            name=item.name,
            description=item.description,
            item_type=item.item_type,
            link=item.link,
            media=item.media.split(),
            created_at=item.created_at
        ) for item in items
    ]


async def get_moodboard(id: int) -> list[Moodboard, list[GetItem]]:
    moodboard = await Moodboard.all(
    ).select_related(
        'author'
    ).get_or_none(id=id)

    if not moodboard:
        raise HTTPException(status_code=404)

    items = await Item.all(
    ).select_related(
        'item_moodboard'
    ).select_related(
        'author'
    ).filter(
        item_moodboard__moodboard=moodboard
    )

    return moodboard, [
        GetItem(
            id=item.id,
            author=UserGet.model_validate(item.author),
            name=item.name,
            description=item.description,
            item_type=item.item_type,
            link=item.link,
            media=item.media.split(),
            created_at=item.created_at
        ) for item in items
    ]


async def get_all_moodboards() -> list[Moodboard]:
    return await Moodboard.all(
    ).select_related(
        'author'
    ).filter(is_private=False)


async def create_item(
    author: User,
    item: CreateItem,
    moodboard: Moodboard | None = None,
) -> GetItem:
    if not moodboard:
        moodboard = await Moodboard.get(author=author, is_chaotic=True)
    created_item = await Item.create(
        **item.model_dump(),
        author=author,
    )
    await ItemMoodboard.create(
        item=created_item,
        moodboard=moodboard,
    )
    return created_item


async def bulk_create_items(
    user: User,
    moodboard: Moodboard,
    items: list[CreateItem],
) -> list[GetItem]:
    created_items = [
        await create_item(user, item, moodboard) for item in items]
    return [
        GetItem(
            id=item.id,
            author=UserGet.model_validate(user),
            name=item.name,
            description=item.description,
            item_type=item.item_type,
            link=item.link,
            media=item.media.split(),
            created_at=item.created_at
        ) for item in created_items
    ]
