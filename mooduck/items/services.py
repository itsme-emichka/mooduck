from fastapi import HTTPException
from tortoise.contrib.postgres.functions import Random
from tortoise.expressions import Q

from moodboards.models import Moodboard
from items.schemas import CreateItem
from items.models import Item, ItemMoodboard, ITEM_TYPES
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


async def update_item(item: Item, data: dict) -> Item:
    try:
        item.update_from_dict(data)
        await item.save()
        return item
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


async def get_item_check_authorization(user: User, item_id: int) -> Item:
    item: Item = await get_item(item_id)
    if item.is_private and user != item.author:
        raise HTTPException(401)
    return item


async def get_random_item(item_type: str | None = None) -> Item:
    if not item_type:
        return await Item.filter(
            is_private=False
        ).select_related(
            'author'
        ).annotate(
            order=Random()
        ).order_by(
            'order'
        ).first()

    if item_type not in ITEM_TYPES.keys():
        raise HTTPException(404, 'incorrect item type')

    return await Item.filter(
        is_private=False
    ).filter(
        item_type=item_type
    ).select_related(
        'author'
    ).annotate(
        order=Random()
    ).order_by(
        'order'
    ).first()


# async def get_all_items(
#     search: str | None = None,
#     item_type: str | None = None
# ) -> list[Item]:
#     if not search:
#         return await Item.filter(
#             is_private=False
#         ).select_related('author')
#     return await Item.filter(
#         is_private=False
#     ).select_related(
#         'author'
#     ).filter(
#         Q(name__icontains=search) | Q(description__icontains=search))


async def get_all_items(
    search: str | None = None,
    item_type: str | None = None
) -> list[Item]:
    items = Item.filter(
        is_private=False
    ).select_related('author')
    if search:
        items = items.filter(
            Q(name__icontains=search) | Q(description__icontains=search))

    if not item_type:
        return await items
    if item_type not in ITEM_TYPES.keys():
        raise HTTPException(400, 'incorrect item type')

    return await items.filter(item_type=item_type)
