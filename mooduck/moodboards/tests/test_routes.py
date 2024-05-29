import pytest


@pytest.mark.asyncio
async def test_create_moodboard_empty(
    moodboard_creation_data_no_items,
    authenticated_client,
):
    response = await authenticated_client.post(
        '/moodboard',
        json=moodboard_creation_data_no_items
    )
    print(response.json())
    assert response.status_code == 200
    assert bool(response.json().get('items')) is False


@pytest.mark.asyncio
async def test_create_moodboard_with_items(
    moodboard_creation_data_new_items,
    authenticated_client
):
    response = await authenticated_client.post(
        '/moodboard',
        json=moodboard_creation_data_new_items
    )
    print(response)
    assert response.status_code == 200
    assert bool(response.json().get('items')) is True


@pytest.mark.asyncio
async def test_create_moodboard_with_existing_items(
    moodboard_creation_data_existing_items,
    authenticated_client
):
    response = await authenticated_client.post(
        '/moodboard',
        json=moodboard_creation_data_existing_items
    )
    print(response.json())
    assert response.status_code == 200
    assert bool(response.json().get('items')) is True
