import pytest
from httpx import AsyncClient, ASGITransport

from main import app
from users.models import User
from extra.utils import get_password_hash, create_access_token


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
async def user_client(user):
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
async def author():
    return await User.create(
        username='author',
        password=get_password_hash('author'),
        email='author@author.com',
        name='author'
    )


@pytest.fixture()
async def author_client(author):
    token = create_access_token(
        data={'sub': author.username}
    )
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url='http://127.0.0.1',
        headers={'Authorization': f'bearer {token}'}
    ) as client:
        print('Client is ready')
        yield client


@pytest.fixture()
def auth_token(user):
    return create_access_token(
        data={'sub': user.username}
    )
