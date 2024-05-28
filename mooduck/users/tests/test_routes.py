import pytest


@pytest.mark.asyncio
async def test_user_creation(client, user_data):
    response = await client.post(
        url='/users',
        json=user_data
    )
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'username': 'user',
        'email': 'user@email.com',
        'name': 'User User',
        'role': 'user',
    }
