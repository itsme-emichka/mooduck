from fastapi import HTTPException
from tortoise.expressions import Q
from tortoise.exceptions import IntegrityError
from tortoise.contrib.postgres.functions import Random

from users.models import User
from moodboards.models import (
    Moodboard,
    FavMoodboard
)
from extra.services import get_instance_or_404
from extra.exceptions import NotAuthorized
from extra.utils import save_image_from_base64
from reactions.models import Comment
from reactions.services import get_moodboard_comments
from items.services import get_moodboard_items
from items.models import Item


# MOODBOARD
async def get_moodboard(id: int) -> Moodboard:
    moodboard = await Moodboard.all(
    ).select_related(
        'author'
    ).get_or_none(id=id)

    if not moodboard:
        raise HTTPException(status_code=404)
    return moodboard


async def get_moodboard_check_authorization(id: int, user: User) -> Moodboard:
    moodboard = await get_moodboard(id)
    if (
        (
            moodboard.is_private or moodboard.is_chaotic
        ) and moodboard.author != user
    ):
        raise HTTPException(401)
    return moodboard


async def get_all_moodboards(search: str | None = None) -> list[Moodboard]:
    if not search:
        return await Moodboard.all(
        ).select_related(
            'author'
        ).filter(
            is_private=False
        )
    return await Moodboard.all(
    ).select_related(
        'author'
    ).filter(
        is_private=False
    ).filter(
        Q(name__icontains=search) | Q(description__icontains=search)
    )


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


async def update_moodboard(moodboard: Moodboard, data: dict) -> Moodboard:
    if data.get('cover', None):
        data['cover'] = save_image_from_base64(data.get('cover', None))
    try:
        moodboard.update_from_dict(data)
        await moodboard.save()
        return moodboard
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


async def get_moodboard_with_items_and_comments(
    id: int,
    user: User
) -> tuple[Moodboard, list[Item], list[Comment]]:
    moodboard = await get_moodboard(id)
    if moodboard.is_private and moodboard.author != user:
        raise NotAuthorized
    return (
        moodboard,
        await get_moodboard_items(moodboard),
        await get_moodboard_comments(moodboard))


async def get_random_moodboard() -> Moodboard:
    return await Moodboard.filter(
        is_private=False
    ).annotate(
        order=Random()
    ).order_by(
        'order'
    ).first(
    ).select_related(
        'author')
