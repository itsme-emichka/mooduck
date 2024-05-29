import pytest
from tortoise import Tortoise
from httpx import AsyncClient, ASGITransport

from main import app
from users.models import User
from extra.utils import get_password_hash, create_access_token
from moodboards.models import Item, Moodboard


# SETUP
async def init_db(
    db_url,
    create_db: bool = False,
    schemas: bool = False
) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url,
        modules={'models': ['users.models', 'moodboards.models']},
        _create_db=create_db
    )
    if schemas:
        await Tortoise.generate_schemas()
        print('Success to generate schemas')


async def init():
    return await init_db('sqlite://db.sqlite3', True, True)


@pytest.fixture(autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()


@pytest.fixture()
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://127.0.0.1'
    ) as client:
        print('Client is ready')
        yield client


# FIXTURES
@pytest.fixture()
def user_data():
    return {
        'username': 'user',
        'password': 'password',
        'email': 'user@email.com',
        'name': 'User User',
        'role': 'user',
        'bio': 'im user'
    }


@pytest.fixture()
async def user():
    return await User.create(
        username='test_user',
        password=get_password_hash('test_password').decode(),
        email='test_email@email.com',
        name='test user',
        role='user',
        bio='test bio'
    )


@pytest.fixture()
async def authenticated_client(user):
    token = create_access_token(
        data={'sub': user.username}
    )
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://127.0.0.1',
        headers={'Authorization': f'bearer {token}'}
    ) as client:
        print('Client is ready')
        yield client


@pytest.fixture()
def item_creation_data():
    return {
        "name": "string",
        "description": "string",
        "item_type": "anime",
        "link": "string",
        "media": [
            "test"
        ]
    }


@pytest.fixture()
def moodboard_creation_data_no_items():
    return {
        "name": "string",
        "description": "string",
        "cover": "string",
        "is_private": False
    }


@pytest.fixture()
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


@pytest.fixture()
def moodboard_creation_data_existing_items(
    moodboard_creation_data_no_items,
    item
):
    return {
        "existing_items": [item.id],
        **moodboard_creation_data_no_items
    }


@pytest.fixture()
async def item(item_creation_data, user):
    return await Item.create(author=user, **item_creation_data)


@pytest.fixture()
def auth_token(user):
    return create_access_token(
        data={'sub': user.username}
    )
