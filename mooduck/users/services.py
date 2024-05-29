from fastapi import HTTPException

from users.models import User, Subscription
from extra.services import get_instance_or_404


async def subscribe_on_user(user: User, sub_for_id: int) -> User:
    sub_for = await get_instance_or_404(User, id=sub_for_id)
    subs, is_created = await Subscription.get_or_create(
        subscriber=user,
        subscribed_for=sub_for
    )
    if not is_created:
        raise HTTPException(400, 'already subscribed')
    return sub_for


async def get_user_subs(user: User) -> list[User]:
    user_subs = await User.all(
    ).select_related(
        'subscribed_for'
    ).filter(subscribed_for__subscriber=user)
    return user_subs


async def delete_user_from_subs(user: User, sub_for_id: int) -> None:
    sub_instance: Subscription = await get_instance_or_404(
        Subscription,
        subscriber=user,
        subscribed_for_id=sub_for_id
    )
    await sub_instance.delete()
    return
