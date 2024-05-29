from fastapi import HTTPException
from tortoise.exceptions import IntegrityError

from users.models import User
from users.schemas import UserGet
from moodboards.models import (
    Moodboard,
    Item,
    ItemMoodboard,
    FavMoodboard
)
from moodboards.schemas import CreateItem, GetItem
from extra.services import get_instance_or_404
from extra.exceptions import NotAuthorized


# MOODBOARD
async def get_moodboard(id: int) -> Moodboard:
    moodboard = await Moodboard.all(
    ).select_related(
        'author'
    ).get_or_none(id=id)

    if not moodboard:
        raise HTTPException(status_code=404)
    return moodboard


async def get_all_moodboards() -> list[Moodboard]:
    return await Moodboard.all(
    ).select_related(
        'author'
    ).filter(is_private=False)


async def get_user_moodboards(
    user: User,
    include_private: bool = False
) -> list[Moodboard]:
    try:
        if include_private:
            return await Moodboard.all(
            ).select_related(
                'author'
            ).filter(author=user)
        return await Moodboard.all(
        ).select_related(
            'author'
        ).filter(author=user, is_private=False)
    except IntegrityError:
        raise HTTPException(404, 'Пользователь не найден')


async def get_chaotic(user: User) -> Moodboard:
    moodboard = await Moodboard.all(
    ).select_related(
        'author'
    ).get_or_none(author=user, is_chaotic=True)

    if not moodboard:
        raise HTTPException(status_code=404)
    return moodboard


async def delete_moodboard(moodboard: Moodboard) -> None:
    if moodboard.is_chaotic:
        raise HTTPException(400, 'Нельзя удалить хаотик')
    try:
        await moodboard.delete()
    except Exception as ex:
        print(ex)
    finally:
        return


async def update_moodboard(moodboard: Moodboard, **kwargs) -> Moodboard:
    try:
        return await moodboard.all().update(**kwargs)
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=400)


# FAV
async def get_user_fav_moodboards(user: User) -> list[Moodboard]:
    return await Moodboard.all(
    ).select_related(
        'fav_moodboard'
    ).select_related(
        'author'
    ).filter(fav_moodboard__user=user)


async def add_moodboard_to_favorite(user: User, moodboard_id: int) -> None:
    moodboard = await get_moodboard(moodboard_id)
    if (
        (
            moodboard.is_chaotic
        ) or (
            moodboard.is_private and moodboard.author != user
        )
    ):
        raise HTTPException(401)

    favmood, is_created = await FavMoodboard.get_or_create(
        user=user,
        moodboard_id=moodboard_id
    )
    if not is_created:
        raise HTTPException(
            status_code=400,
            detail='Уже в избранном'
        )


async def remove_moodboard_from_fav(user: User, moodboard_id: int) -> None:
    instance = await get_instance_or_404(
        FavMoodboard,
        user=user,
        moodboard_id=moodboard_id
    )
    await instance.all().delete()
    return


async def get_user_subs_moodboards(user: User) -> list[Moodboard]:
    subscriptions = await User.all(
    ).select_related(
        'subscribed_for'
    ).filter(
        subscribed_for__subscriber=user
    ).values_list('id', flat=True)

    moodboards = await Moodboard.all(
    ).select_related(
        'author'
    ).filter(
        author_id__in=subscriptions,
        is_private=False,
        is_chaotic=False,
    )
    return moodboards


# ITEMS
async def add_existing_items_to_moodboard(
    id_list: list[int],
    moodboard: Moodboard
) -> list[GetItem]:
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


async def get_moodboard_items(moodboard: Moodboard) -> list[GetItem]:
    items = await Item.all(
    ).select_related(
        'item_moodboard'
    ).select_related(
        'author'
    ).filter(
        item_moodboard__moodboard=moodboard
    )

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


async def get_moodboard_with_items(
    id: int,
    user: User
) -> tuple[Moodboard, list[GetItem]]:
    moodboard = await get_moodboard(id)
    if moodboard.is_private and moodboard.author != user:
        raise NotAuthorized
    return moodboard, await get_moodboard_items(moodboard)


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
