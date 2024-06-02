import pytest

from reactions.models import Comment


@pytest.fixture()
async def comment(author, moodboard):
    return await Comment.create(
        author=author,
        moodboard=moodboard,
        text='text'
    )


@pytest.fixture()
async def comments(author, moodboard):
    first_comment = await Comment.create(
        author=author,
        moodboard=moodboard,
        text='first_comment'
    )
    second_comment = await Comment.create(
        author=author,
        moodboard=moodboard,
        text='second_comment'
    )
    third_comment = await Comment.create(
        author=author,
        moodboard=moodboard,
        text='third_comment'
    )
    fourth_comment = await Comment.create(
        author=author,
        moodboard=moodboard,
        text='fourth_comment'
    )
    return first_comment, second_comment, third_comment, fourth_comment
