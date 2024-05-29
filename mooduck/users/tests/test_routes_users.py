import pytest


@pytest.mark.asyncio
async def test_user_creation(client, user_data):
    response = await client.post(
        url='/user',
        json=user_data
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'username': 'user',
        'email': 'user@email.com',
        'name': 'User User',
        'role': 'user',
        'bio': 'im user'
    }


@pytest.mark.asyncio
async def test_users_me(authenticated_client):
    response = await authenticated_client.get('/user/me')
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'username': 'test_user',
        'email': 'test_email@email.com',
        'name': 'test user',
        'role': 'user',
        'bio': 'test bio'
    }


@pytest.mark.asyncio
async def test_users_me_not_auth(client):
    response = await client.get('/user/me')
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_auth(user, client):
    response = await client.post(
        url='/auth',
        data={
            'username': user.username,
            'password': 'test_password'
        }
    )
    assert response.status_code == 200
