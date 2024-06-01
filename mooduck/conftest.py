import pytest
from tortoise import Tortoise

from tests.conftest_utils.users_conf import *
from tests.conftest_utils.moodboards_conf import *


# SETUP
async def init_db(
    db_url,
    create_db: bool = False,
    schemas: bool = False
) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url,
        modules={
            'models': [
                'users.models',
                'moodboards.models',
                'items.models',
                'reactions.models'
            ]
        },
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
