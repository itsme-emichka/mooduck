from pprint import pprint

import pytest


pytestmark = pytest.mark.asyncio


async def test_add_items_to_chaotic(
    user_client,
    user_chaotic,
    item_creation_data
):
    response = await user_client.post(
        '/chaotic',
        json={
            'items': [item_creation_data]
        }
    )
    pprint(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_add_existing_items_to_chaotic(
    user_client,
    user_chaotic,
    item
):
    response = await user_client.post(
        '/chaotic',
        json={
            'existing_items': [item.id]
        }
    )
    pprint(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get('id') == item.id


async def test_add_existing_items_to_chaotic_400(
    user_client,
    user_chaotic,
    item
):
    response = await user_client.post(
        '/chaotic',
        json={
            'existing_items': [item.id + 1]
        }
    )
    pprint(response.json())
    assert response.status_code == 400


async def test_delete_item_from_chaotic(
    user_client,
    user_with_chaotic
):
    user, chaotic, item = user_with_chaotic
    response = await user_client.delete(f'/chaotic/{item.id}')
    assert response.status_code == 204
    response = await user_client.get('/chaotic')
    assert response.status_code == 200
    assert len(response.json().get('items')) == 0


async def test_delete_item_from_chaotic_404(
    user_client,
    user_with_chaotic
):
    user, chaotic, item = user_with_chaotic
    response = await user_client.delete(f'/chaotic/{item.id + 1}')
    assert response.status_code == 404
    response = await user_client.get('/chaotic')
    assert response.status_code == 200
    assert len(response.json().get('items')) == 1


async def test_add_items_to_moodboard(
    author_client,
    author,
    moodboard,
    item_creation_data
):
    response = await author_client.post(
        f'/moodboard/{moodboard.id}/item',
        json={'items': [item_creation_data]}
    )
    pprint(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get('name') == 'string'


async def test_add_existing_items_to_moodboard(
    author_client,
    author,
    moodboard,
    item
):
    response = await author_client.post(
        f'/moodboard/{moodboard.id}/item',
        json={'existing_items': [item.id]}
    )
    pprint(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0].get('name') == 'string'


async def test_add_items_to_moodboard_401(
    user_client,
    moodboard,
    item_creation_data
):
    response = await user_client.post(
        f'/moodboard/{moodboard.id}/item',
        json={'items': [item_creation_data]}
    )
    pprint(response.json())
    assert response.status_code == 401


async def test_get_moodboard_items(
    user_client,
    moodboard_item_comment,
):
    moodboard, item, comment = moodboard_item_comment
    response = await user_client.get(f'/moodboard/{moodboard.id}/item')
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_private_moodboard_items(
    private_moodboard,
    user_client
):
    response = await user_client.get(f'/moodboard/{private_moodboard.id}/item')
    assert response.status_code == 401


async def test_delete_item_from_moodboard(
    author_client,
    moodboard_item_comment
):
    moodboard, item, comment = moodboard_item_comment
    response = await author_client.delete(
        f'/moodboard/{moodboard.id}/item/{item.id}')
    assert response.status_code == 204
    response = await author_client.get(f'/moodboard/{moodboard.id}/item')
    assert len(response.json()) == 0


async def test_delete_item_from_moodboard_401(
    user_client,
    moodboard_item_comment
):
    moodboard, item, comment = moodboard_item_comment
    response = await user_client.delete(
        f'/moodboard/{moodboard.id}/item/{item.id}')
    assert response.status_code == 401
    response = await user_client.get(f'/moodboard/{moodboard.id}/item')
    assert len(response.json()) == 1


async def test_delete_item_from_moodboard_404(
    author_client,
    moodboard_item_comment
):
    moodboard, item, comment = moodboard_item_comment
    response = await author_client.delete(
        f'/moodboard/{moodboard.id}/item/{item.id + 1}')
    assert response.status_code == 404
    response = await author_client.get(f'/moodboard/{moodboard.id}/item')
    assert len(response.json()) == 1


async def test_retrieve_item(
    user_client,
    item
):
    response = await user_client.get(f'/item/{item.id}')
    assert response.status_code == 200
    assert response.json().get('id') == item.id


async def test_retrieve_private_item(
    author_client,
    private_item
):
    response = await author_client.get(f'/item/{private_item.id}')
    assert response.status_code == 200
    assert response.json().get('id') == private_item.id


async def test_retrieve_private_item_401(
    user_client,
    private_item
):
    response = await user_client.get(f'/item/{private_item.id}')
    assert response.status_code == 401


async def test_random_item(user_client, items):
    first_item, second_item, third_item, fourth_item = items
    response = await user_client.get('/random/item')
    assert response.status_code == 200
    assert response.json().get('id') in (
        first_item.id,
        second_item.id,
        third_item.id,
        fourth_item.id
    )


async def test_patch_item(author_client, item):
    response = await author_client.patch(
        f'/item/{item.id}',
        json={
            'name': 'patched'
        }
    )
    assert response.status_code == 200
    assert response.json().get('name') == 'patched'
    assert len(response.json().get('media')) == 1


async def test_patch_item_media(author_client, item):
    response = await author_client.patch(
        f'/item/{item.id}',
        json={
            'media': ['data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7']
        }
    )
    assert response.status_code == 200
    assert len(response.json().get('media')) == 1


async def test_patch_item_401(user_client, item):
    response = await user_client.patch(
        f'/item/{item.id}',
        json={
            'name': 'patched'
        }
    )
    assert response.status_code == 401
    response = await user_client.get(f'/item/{item.id}')
    assert response.json().get('name') == item.name


async def test_list_item(user_client, items):
    first_item, second_item, third_item, fourth_item = items
    response = await user_client.get('/item')
    pprint(response.json())
    json: dict = response.json()
    items = json.get('items')
    assert response.status_code == 200
    assert len(items) == 4
    assert items[0].get('id') == fourth_item.id
    assert json.get('next_page') is None
    assert json.get('prev_page') is None


async def test_list_items_with_params(user_client, items):
    first_item, second_item, third_item, fourth_item = items
    response_limit = await user_client.get('/item?limit=2')
    response_limit_page = await user_client.get('/item?limit=2&page=2')

    response_limit_json = response_limit.json()
    response_limit_page_json = response_limit_page.json()

    assert response_limit.status_code == 200
    assert response_limit_page.status_code == 200

    assert len(response_limit_json.get('items')) == 2
    assert len(response_limit_page_json.get('items')) == 2

    assert response_limit_json.get('prev_page') is None
    assert response_limit_page_json.get('prev_page') is not None

    assert response_limit_json.get('next_page') is not None
    assert response_limit_page_json.get('next_page') is None

    assert response_limit_json.get('items')[0].get('id') == fourth_item.id
    assert response_limit_page_json.get('items')[0].get('id') == second_item.id
