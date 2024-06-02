from datetime import datetime, timedelta

from tortoise.expressions import Q
from tortoise.contrib.postgres.functions import Random
from tortoise.queryset import QuerySet

from users.models import User
from moodboards.models import (
    Moodboard,
    FavMoodboard
)
from extra.services import get_instance_or_404
from extra.exceptions import UnAuthorized, NotFound, BadRequest
from extra.utils import save_image_from_base64
from reactions.models import Comment
from reactions.services import get_moodboard_comments
from items.services import get_moodboard_items
from items.models import Item
from moodboards.exceptions import AlreadyInFavorite, CantDeleteChaotic


# MOODBOARD
async def get_moodboard(id: int) -> Moodboard:
    moodboard = await Moodboard.all(
    ).select_related(
        'author'
    ).get_or_none(id=id)

    if not moodboard:
        raise NotFound
    return moodboard


async def get_moodboard_check_authorization(id: int, user: User) -> Moodboard:
    moodboard = await get_moodboard(id)
    if (
        (
            moodboard.is_private or moodboard.is_chaotic
        ) and moodboard.author != user
    ):
        raise UnAuthorized
    return moodboard


def get_user_moodboards(
    user: User,
    include_private: bool = False
) -> QuerySet[Moodboard]:
    base_query = Moodboard.all(
    ).select_related(
        'author'
    ).filter(author=user)
    if not include_private:
        base_query = base_query.filter(is_private=False)
    return base_query


async def get_chaotic(user: User) -> Moodboard:
    moodboard = await Moodboard.all(
    ).select_related(
        'author'
    ).get_or_none(author=user, is_chaotic=True)

    if not moodboard:
        raise NotFound
    return moodboard


async def delete_moodboard(moodboard: Moodboard) -> None:
    if moodboard.is_chaotic:
        raise CantDeleteChaotic
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
        raise BadRequest


# FAV
def get_user_fav_moodboards(user: User) -> QuerySet[Moodboard]:
    return Moodboard.all(
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
        raise UnAuthorized

    favmood, is_created = await FavMoodboard.get_or_create(
        user=user,
        moodboard_id=moodboard_id
    )
    if not is_created:
        raise AlreadyInFavorite


async def remove_moodboard_from_fav(user: User, moodboard_id: int) -> None:
    instance = await get_instance_or_404(
        FavMoodboard,
        user=user,
        moodboard_id=moodboard_id
    )
    await instance.all().delete()


async def get_user_subs_moodboards(user: User) -> QuerySet[Moodboard]:
    subscriptions = await User.all(
    ).select_related(
        'subscribed_for'
    ).filter(
        subscribed_for__subscriber=user
    ).values_list('id', flat=True)

    moodboards = Moodboard.all(
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
        raise UnAuthorized
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


def get_moodboards(
    search: str | None,
    sort: str = 'created_at',
    period_from: int = 30,
    period_to: int = 0,
) -> QuerySet[Moodboard]:
    period_to = datetime.now() - timedelta(days=period_to)
    period_from = period_to - timedelta(days=period_from)

    base_query = Moodboard.all(
    ).select_related(
        'author'
    ).filter(
        created_at__gte=period_from,
        created_at__lte=period_to
    ).order_by(
        f'-{sort}',
        '-created_at'
    )
    if search:
        base_query = base_query.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )
    return base_query
