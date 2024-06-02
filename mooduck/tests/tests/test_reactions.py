from pprint import pprint

import pytest


pytestmark = pytest.mark.asyncio


async def test_post_comment(author_client, author, moodboard):
    response = await author_client.post(
        f'/moodboard/{moodboard.id}/comment',
        json={
            'text': 'test comment'
        }
    )
    json = response.json()
    pprint(json)
    assert response.status_code == 200
    assert len(json) == 1
    assert json[0].get('text') == 'test comment'
    assert json[0].get('answering_to') is None
    assert json[0].get('author').get('id') == author.id


async def test_post_comment_answer(
    user_client,
    user,
    author,
    comment,
    moodboard
):
    response = await user_client.post(
        f'/moodboard/{moodboard.id}/comment/{comment.id}',
        json={
            'text': 'test comment'
        }
    )
    json = response.json()
    pprint(json)
    assert response.status_code == 200
    assert len(json) == 2
    assert json[0].get('text') == 'text'
    assert json[0].get('author').get('id') == author.id
    assert json[0].get('answering_to') is None
    assert json[1].get('answering_to') == comment.id
    assert json[1].get('author').get('id') == user.id


async def test_list_comment(user_client, moodboard, comments):
    first_comment, second_comment, third_comment, fourth_comment = comments
    response = await user_client.get(f'/moodboard/{moodboard.id}/comment')
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 4
    assert json[0].get('id') == first_comment.id


async def test_retrieve_comment(user_client, moodboard, comment):
    response = await user_client.get(
        f'/moodboard/{moodboard.id}/comment/{comment.id}')
    assert response.status_code == 200
    assert response.json().get('id') == comment.id


async def test_retrieve_comment_404(user_client, moodboard, comment):
    response = await user_client.get(
        f'/moodboard/{moodboard.id}/comment/{comment.id + 1}')
    assert response.status_code == 404


async def test_patch_comment(author_client, moodboard, comment):
    response = await author_client.patch(
        f'/moodboard/{moodboard.id}/comment/{comment.id}',
        json={'text': 'patched'}
    )
    assert response.status_code == 200
    assert response.json().get('text') == 'patched'


async def test_patch_comment_401(user_client, moodboard, comment):
    response = await user_client.patch(
        f'/moodboard/{moodboard.id}/comment/{comment.id}',
        json={'text': 'patched'}
    )
    assert response.status_code == 401


async def test_patch_comment_404(author_client, moodboard, comment):
    response = await author_client.patch(
        f'/moodboard/{moodboard.id}/comment/{comment.id + 1}',
        json={'text': 'patched'}
    )
    assert response.status_code == 404


async def test_delete_comment(author_client, moodboard, comment):
    response = await author_client.delete(
        f'/moodboard/{moodboard.id}/comment/{comment.id}')
    assert response.status_code == 204


async def test_delete_comment_404(author_client, moodboard, comment):
    response = await author_client.delete(
        f'/moodboard/{moodboard.id}/comment/{comment.id + 1}')
    assert response.status_code == 404


async def test_delete_comment_401(user_client, moodboard, comment):
    response = await user_client.delete(
        f'/moodboard/{moodboard.id}/comment/{comment.id}')
    assert response.status_code == 401


async def test_like(user_client, moodboard):
    response = await user_client.post(f'/moodboard/{moodboard.id}/like')
    assert response.status_code == 204
    response = await user_client.post(f'/moodboard/{moodboard.id}/like')
    assert response.status_code == 400

    response = await user_client.get(f'/moodboard/{moodboard.id}')
    assert response.json().get('likes') == 1
    assert response.json().get('is_liked') is True

    response = await user_client.delete(f'/moodboard/{moodboard.id}/like')
    assert response.status_code == 204
    response = await user_client.delete(f'/moodboard/{moodboard.id}/like')
    assert response.status_code == 404

    response = await user_client.get(f'/moodboard/{moodboard.id}')
    assert response.json().get('likes') == 0
    assert response.json().get('is_liked') is False
