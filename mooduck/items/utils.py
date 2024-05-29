from items.models import Item
from items.schemas import GetItem
from users.schemas import UserGet


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
        is_private=item.is_private,
        media=item.media.split(),
        created_at=item.created_at
    )


def get_item_list_response(
    items: list[Item]
) -> list[GetItem]:
    return [get_item_response(item) for item in items]
