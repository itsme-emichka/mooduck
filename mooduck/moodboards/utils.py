from users.schemas import UserGet
from moodboards.models import Moodboard, Item
from moodboards.schemas import GetMoodboard, GetItem
from reactions.models import Comment
from reactions.utils import get_comment_list_response


def get_moodboard_response(
    moodboard: Moodboard,
    items: list[Item],
    comments: list[Comment],
) -> GetMoodboard:
    return GetMoodboard(
        id=moodboard.id,
        author=moodboard.author,
        name=moodboard.name,
        description=moodboard.description,
        cover=moodboard.cover,
        is_private=moodboard.is_private,
        is_chaotic=moodboard.is_chaotic,
        created_at=moodboard.created_at,
        items=get_item_list_response(items),
        comments=get_comment_list_response(comments)
    )


def get_item_response(
    item: Item
) -> GetItem:
    return GetItem(
        id=item.id,
        author=UserGet.model_validate(item.author),
        name=item.name,
        description=item.description,
        item_type=item.item_type,
        link=item.link,
        media=item.media.split(),
        created_at=item.created_at
    )


def get_item_list_response(
    items: list[Item]
) -> list[GetItem]:
    return [get_item_response(item) for item in items]
