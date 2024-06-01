from pprint import pprint

import pytest


pytestmark = pytest.mark.asyncio


async def test_create_moodboard_empty(
    moodboard_creation_data_no_items,
    user_client,
):
    response = await user_client.post(
        '/moodboard',
        json=moodboard_creation_data_no_items
    )
    print(response.json())
    assert response.status_code == 200
    assert bool(response.json().get('items')) is False


async def test_create_moodboard_with_items(
    moodboard_creation_data_new_items,
    user_client
):
    response = await user_client.post(
        '/moodboard',
        json=moodboard_creation_data_new_items
    )
    print(response)
    assert response.status_code == 200
    assert bool(response.json().get('items')) is True


async def test_create_moodboard_with_existing_items(
    moodboard_creation_data_existing_items,
    user_client
):
    response = await user_client.post(
        '/moodboard',
        json=moodboard_creation_data_existing_items
    )
    print(response.json())
    assert response.status_code == 200
    assert bool(response.json().get('items')) is True


async def test_retrieve_moodboard(moodboard_item_comment, user_client):
    moodboard, item, comment = moodboard_item_comment
    response = await user_client.get(f'/moodboard/{moodboard.id}')
    print(response.json())
    assert response.status_code == 200
    assert bool(response.json().get('items')) is True
    assert bool(response.json().get('comments')) is True


async def test_retrieve_private_moodboard(user_client, private_moodboard):
    response = await user_client.get(f'/moodboard/{private_moodboard.id}')
    assert response.status_code == 401


async def test_retrieve_moodboard_404(moodboard_item_comment, user_client):
    moodboard, item, comment = moodboard_item_comment
    response = await user_client.get(f'/moodboard/{moodboard.id + 1}')
    print(response.json())
    assert response.status_code == 404


async def test_retrieve_moodboard_401(moodboard_item_comment, client):
    moodboard, item, comment = moodboard_item_comment
    response = await client.get(f'/moodboard/{moodboard.id}')
    print(response.json())
    assert response.status_code == 401


async def test_delete_moodboard(author_client, moodboard_item_comment):
    moodboard, item, comment = moodboard_item_comment
    response = await author_client.delete(f'/moodboard/{moodboard.id}')
    assert response.status_code == 204


async def test_delete_moodboard_404(author_client, moodboard_item_comment):
    moodboard, item, comment = moodboard_item_comment
    response = await author_client.delete(f'/moodboard/{moodboard.id + 1}')
    print(response.json())
    assert response.status_code == 404


async def test_delete_moodboard_401(user_client, moodboard_item_comment):
    moodboard, item, comment = moodboard_item_comment
    response = await user_client.delete(f'/moodboard/{moodboard.id}')
    print(response.json())
    assert response.status_code == 401


async def test_delete_moodboard_401_not_auth(client, moodboard_item_comment):
    moodboard, item, comment = moodboard_item_comment
    response = await client.delete(f'/moodboard/{moodboard.id}')
    print(response.json())
    assert response.status_code == 401


async def test_moodboard_patch(author_client, moodboard_item_comment):
    moodboard, item, comment = moodboard_item_comment
    response = await author_client.patch(
        f'/moodboard/{moodboard.id}',
        json={
            'name': 'patched'
        }
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json().get('name') == 'patched'


async def test_moodboard_patch_404(author_client, moodboard_item_comment):
    moodboard, item, comment = moodboard_item_comment
    response = await author_client.patch(
        f'/moodboard/{moodboard.id + 1}',
        json={
            'name': 'patched'
        }
    )
    print(response.json())
    assert response.status_code == 404


async def test_moodboard_patch_401(user_client, moodboard_item_comment):
    moodboard, item, comment = moodboard_item_comment
    response = await user_client.patch(
        f'/moodboard/{moodboard.id}',
        json={
            'name': 'patched'
        }
    )
    print(response.json())
    assert response.status_code == 401


async def test_moodboard_patch_401_not_auth(client, moodboard_item_comment):
    moodboard, item, comment = moodboard_item_comment
    response = await client.patch(
        f'/moodboard/{moodboard.id}',
        json={
            'name': 'patched'
        }
    )
    print(response.json())
    assert response.status_code == 401


async def test_list_moodboard_401_not_auth(client, moodboards):
    first_mb, second_mb, third_mb, fourth_mb = moodboards
    response = await client.get('/moodboard')
    assert response.status_code == 401


async def test_list_moodboard(user_client, moodboards):
    first_mb, second_mb, third_mb, fourth_mb = moodboards
    response = await user_client.get('/moodboard')
    print(response.json())
    assert response.status_code == 200
    assert response.json().get('items')[0].get('id') == fourth_mb.id
    assert response.json().get('items')[1].get('id') == third_mb.id
    assert response.json().get('items')[2].get('id') == second_mb.id
    assert len(response.json().get('items')) == 3


async def test_list_moodboard_week(user_client, moodboards):
    first_mb, second_mb, third_mb, fourth_mb = moodboards
    response = await user_client.get('/moodboard?period_from=7')
    pprint(response.json())
    assert response.status_code == 200
    assert response.json().get('items')[0].get('id') == fourth_mb.id
    assert response.json().get('items')[1].get('id') == third_mb.id
    assert len(response.json().get('items')) == 2


async def test_list_moodboard_day(user_client, moodboards):
    first_mb, second_mb, third_mb, fourth_mb = moodboards
    response = await user_client.get('/moodboard?period_from=1')
    pprint(response.json())
    assert response.status_code == 200
    assert response.json().get('items')[0].get('id') == fourth_mb.id
    assert len(response.json().get('items')) == 1


async def test_list_moodboard_by_likes(user_client, moodboards):
    first_mb, second_mb, third_mb, fourth_mb = moodboards
    response = await user_client.get('/moodboard?sort=likes')
    print(response.json())
    assert response.status_code == 200
    assert response.json().get('items')[0].get('id') == second_mb.id
    assert response.json().get('items')[1].get('id') == third_mb.id
    assert response.json().get('items')[2].get('id') == fourth_mb.id


async def test_user_moodboards(user_client, author, moodboards):
    first_mb, second_mb, third_mb, fourth_mb = moodboards
    response = await user_client.get(f'/user/{author.id}/moodboard')
    assert response.status_code == 200
    assert len(response.json().get('items')) == 4


async def test_user_moodboards_slf(author_client, moodboards):
    first_mb, second_mb, third_mb, fourth_mb = moodboards
    response = await author_client.get('/user/me/moodboard')
    assert response.status_code == 200
    assert len(response.json().get('items')) == 4


async def test_user_moodboards_slf_empty(user_client, moodboards):
    first_mb, second_mb, third_mb, fourth_mb = moodboards
    response = await user_client.get('/user/me/moodboard')
    assert response.status_code == 200
    assert len(response.json().get('items')) == 0


async def test_search_moodboard(user_client, moodboards):
    first_mb, second_mb, third_mb, fourth_mb = moodboards
    response = await user_client.get(f'/moodboard?search={fourth_mb.name}')
    pprint(response.json())
    assert response.status_code == 200
    assert response.json().get('items')[0].get('id') == fourth_mb.id


async def test_random_moodboard(user_client, moodboards):
    first_mb, second_mb, third_mb, fourth_mb = moodboards
    response = await user_client.get('random/moodboard')
    assert response.status_code == 200
    assert response.json().get('id') in (
        first_mb.id,
        second_mb.id,
        third_mb.id,
        fourth_mb.id
    )


async def test_user_fav_moodboards(user_fav_moodboard, user_client):
    user, moodboard = user_fav_moodboard
    response = await user_client.get('/fav')
    assert response.status_code == 200
    assert len(response.json().get('items')) == 1
    assert response.json().get('items')[0].get('id') == moodboard.id


async def test_moodboard_add_to_fav(user_client, moodboard):
    response = await user_client.post(f'/moodboard/{moodboard.id}/fav')
    assert response.status_code == 200
    response = await user_client.get('/fav')
    assert response.status_code == 200
    assert len(response.json().get('items')) == 1
    assert response.json().get('items')[0].get('id') == moodboard.id


async def test_delete_moodboard_from_fav(user_fav_moodboard, user_client):
    user, moodboard = user_fav_moodboard
    response = await user_client.delete(f'/moodboard/{moodboard.id}/fav')
    assert response.status_code == 200
    response = await user_client.get('/fav')
    assert len(response.json().get('items')) == 0


async def test_delete_moodboard_from_fav_404(user_fav_moodboard, user_client):
    user, moodboard = user_fav_moodboard
    response = await user_client.delete(f'/moodboard/{moodboard.id + 1}/fav')
    assert response.status_code == 404
    response = await user_client.get('/fav')
    assert response.json().get('items')[0].get('id') == moodboard.id


async def test_sub_moodboards(user_sub_author, user_client):
    user, author, moodboards = user_sub_author
    response = await user_client.get('/sub/moodboard')
    assert response.status_code == 200
    assert len(response.json().get('items')) == 4


async def test_user_chaotic(user_with_chaotic, user_client):
    user, chaotic, item = user_with_chaotic
    response = await user_client.get('/chaotic')
    assert response.status_code == 200
    assert len(response.json().get('items')) == 1
    assert response.json().get('items')[0].get('id') == chaotic.id
