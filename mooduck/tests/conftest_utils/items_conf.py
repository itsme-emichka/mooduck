import datetime

import pytest

from items.models import Item


@pytest.fixture()
def item_creation_data(base64):
    return {
        "name": "string",
        "description": "string",
        "item_type": "anime",
        "link": "string",
        "media": [
            base64
        ]
    }


@pytest.fixture()
async def item(item_creation_data, author):
    return await Item.create(author=author, **item_creation_data)


@pytest.fixture()
async def private_item(author):
    return await Item.create(
        author=author,
        name='private item',
        item_type='anime',
        is_private=True
    )


@pytest.fixture()
async def items(author):
    first_item = await Item.create(
        author=author,
        name='first item',
        item_type='anime',
        created_at=datetime.datetime.now() - datetime.timedelta(days=35)
    )
    second_item = await Item.create(
        author=author,
        name='second item',
        item_type='anime',
        created_at=datetime.datetime.now() - datetime.timedelta(days=20)
    )
    third_item = await Item.create(
        author=author,
        name='third item',
        item_type='anime',
        created_at=datetime.datetime.now() - datetime.timedelta(days=5)
    )
    fourth_item = await Item.create(
        author=author,
        name='fourth item',
        item_type='anime',
        created_at=datetime.datetime.now() - datetime.timedelta(days=1)
    )
    return first_item, second_item, third_item, fourth_item
