from tortoise.contrib.postgres.functions import Random
from tortoise.expressions import Q

from moodboards.models import Moodboard
from items.schemas import CreateItem
from items.utils import get_media_from_base64_list
from items.models import Item, ItemMoodboard, ITEM_TYPES
from users.models import User
from extra.exceptions import NotFound, UnAuthorized


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
        name=item.name,
        item_type=item.item_type,
        description=item.description,
        link=item.link,
        is_private=item.is_private,
        media=get_media_from_base64_list(item.media),
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
        raise NotFound
    return item


async def update_item(item: Item, data: dict) -> Item:
    if data.get('media', None):
        data['media'] = get_media_from_base64_list(data.get('media'))
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
        raise NotFound

    await ItemMoodboard.filter(
        moodboard=moodboard,
        item_id=item_id
    ).delete()
    if delete_item:
        pass


async def get_item_check_authorization(user: User, item_id: int) -> Item:
    item: Item = await get_item(item_id)
    if item.is_private and user != item.author:
        raise UnAuthorized
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
        raise NotFound

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


def get_all_items(
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
        return items
    if item_type not in ITEM_TYPES.keys():
        raise NotFound

    return items.filter(item_type=item_type)
