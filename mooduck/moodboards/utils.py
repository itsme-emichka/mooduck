from users.models import User
from moodboards.models import Moodboard
from moodboards.schemas import GetMoodboard, GetItem


def get_moodboard_response(
    moodboard: Moodboard,
    items: list[GetItem],
    author: User
) -> GetMoodboard:
    return GetMoodboard(
        id=moodboard.id,
        author=author,
        name=moodboard.name,
        description=moodboard.description,
        cover=moodboard.cover,
        is_private=moodboard.is_private,
        is_chaotic=moodboard.is_chaotic,
        created_at=moodboard.created_at,
        items=items
    )
