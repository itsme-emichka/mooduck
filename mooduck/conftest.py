import pytest
from tortoise import Tortoise
from httpx import AsyncClient, ASGITransport

from main import app


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
