from fastapi import HTTPException

from moodboards.models import Moodboard
from items.schemas import CreateItem
from items.models import Item, ItemMoodboard
from users.models import User


async def add_existing_items_to_moodboard(
    id_list: list[int],
    moodboard: Moodboard
) -> list[Item]:
    moodboard_items_ids = await Item.all(
    ).select_related(
        'item_moodboard'
    ).filter(
        item_moodboard__moodboard=moodboard
    ).values_list('id', flat=True)
    diff = set(id_list).difference(set(moodboard_items_ids))
    if not diff:
        return []

    items = await Item.filter(id__in=diff).select_related('author')

    await ItemMoodboard.bulk_create(
        [ItemMoodboard(
            item=item, moodboard=moodboard
            ) for item in items])
    return items


async def get_moodboard_items(moodboard: Moodboard) -> list[Item]:
    return await Item.all(
    ).select_related(
        'item_moodboard'
    ).select_related(
        'author'
    ).filter(
        item_moodboard__moodboard=moodboard
    )


async def create_item(
    author: User,
    item: CreateItem,
    moodboard: Moodboard | None = None,
) -> Item:
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


async def get_item(item_id: int) -> Item:
    item = await Item.all().select_related('author').get_or_none(id=item_id)
    if not item:
        raise HTTPException(404)
    return item


async def update_item(item: Item, **kwargs) -> Item:
    try:
        await item.all().update(**kwargs)
    except Exception as ex:
        print(ex)
    finally:
        return await get_item(item.id)


async def bulk_create_items(
    user: User,
    moodboard: Moodboard,
    items: list[CreateItem],
) -> list[Item]:
    return [
        await create_item(user, item, moodboard) for item in items]


async def delete_item_from_moodboard(
    user: User,
    moodboard: Moodboard,
    item_id: int,
    delete_item: bool = False,
) -> None:
    moodboard_items_ids = await ItemMoodboard.all(
    ).filter(
        moodboard=moodboard
    ).values_list('item_id', flat=True)

    if item_id not in moodboard_items_ids:
        raise HTTPException(404)

    await ItemMoodboard.filter(
        moodboard=moodboard,
        item_id=item_id
    ).delete()
    if delete_item:
        pass
