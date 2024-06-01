import datetime

import pytest_asyncio

from items.models import ItemMoodboard
from moodboards.models import Moodboard, FavMoodboard
from reactions.models import Comment
from users.models import Subscription


@pytest_asyncio.fixture()
def moodboard_creation_data_no_items(base64):
    return {
        "name": "string",
        "description": "string",
        "cover": base64,
        "is_private": False
    }


@pytest_asyncio.fixture()
def moodboard_creation_data_new_items(
    moodboard_creation_data_no_items,
    item_creation_data
):
    return {
        "items": [
            item_creation_data
        ],
        **moodboard_creation_data_no_items
    }


@pytest_asyncio.fixture()
def moodboard_creation_data_existing_items(
    moodboard_creation_data_no_items,
    item
):
    return {
        "existing_items": [item.id],
        **moodboard_creation_data_no_items
    }


@pytest_asyncio.fixture()
async def comment(author, moodboard):
    return await Comment.create(
        author=author,
        moodboard=moodboard,
        text='test comment'
    )


@pytest_asyncio.fixture()
async def moodboard(author):
    return await Moodboard.create(
        author=author,
        name='moodboard',
        description='moodboard'
    )


@pytest_asyncio.fixture()
async def moodboard_item_comment(moodboard, item, comment):
    await ItemMoodboard.create(item=item, moodboard=moodboard)
    return moodboard, item, comment


@pytest_asyncio.fixture()
async def moodboards(author):
    first_mb = await Moodboard.create(
        author=author,
        name='first',
        likes=9,
        created_at=datetime.datetime.now() - datetime.timedelta(days=35)
    )
    second_mb = await Moodboard.create(
        author=author,
        name='second',
        likes=6,
        created_at=datetime.datetime.now() - datetime.timedelta(days=20)
    )
    third_mb = await Moodboard.create(
        author=author,
        name='third',
        likes=3,
        created_at=datetime.datetime.now() - datetime.timedelta(days=5)
    )
    fourth_mb = await Moodboard.create(
        author=author,
        name='fourth',
        likes=0,
    )
    return first_mb, second_mb, third_mb, fourth_mb


@pytest_asyncio.fixture()
async def user_fav_moodboard(user, moodboard):
    await FavMoodboard.create(
        user=user,
        moodboard=moodboard
    )
    return user, moodboard


@pytest_asyncio.fixture()
async def user_sub_author(user, author, moodboards):
    await Subscription.create(
        subscriber=user,
        subscribed_for=author
    )
    return user, author, moodboards


@pytest_asyncio.fixture()
async def user_chaotic(user):
    return await Moodboard.create(
        author=user,
        name=f'{user.username}ын Хаотик',
        is_chaotic=True,
        is_private=True
    )


@pytest_asyncio.fixture()
async def user_with_chaotic(user_chaotic, item, user):
    await ItemMoodboard.create(
        item=item,
        moodboard=user_chaotic
    )
    return user, user_chaotic, item


@pytest_asyncio.fixture()
async def private_moodboard(author):
    return await Moodboard.create(
        author=author,
        name='private',
        is_private=True
    )
