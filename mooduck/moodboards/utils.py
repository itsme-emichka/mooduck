from moodboards.models import Moodboard
from moodboards.schemas import GetMoodboard
from reactions.models import Comment
from reactions.utils import get_comment_list_response
from items.utils import get_item_list_response
from items.models import Item


def get_moodboard_response(
    moodboard: Moodboard,
    items: list[Item],
    comments: list[Comment],
    is_liked: bool = False,
    is_in_favorite: bool = False
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
        comments=get_comment_list_response(comments),
        likes=moodboard.likes,
        is_liked=is_liked,
        is_in_favorite=is_in_favorite
    )
