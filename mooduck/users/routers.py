from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
import bcrypt

from users.schemas import UserCreate, UserGet, PaginatedUser
from users.models import User
from users.services import (
    subscribe_on_user as subscribe_on_user_db,
    get_user_subs,
    delete_user_from_subs,
    get_all_users
)
from users.exceptions import WrongLoginOrPassword
from moodboards.models import Moodboard
from extra.services import create_instance_by_kwargs, get_instance_or_404
from extra.utils import get_password_hash, create_access_token
from extra.dependencies import is_authenticated, pagination


router = APIRouter()
oauth_scheme = OAuth2PasswordBearer('auth', auto_error=True)


@router.post('/user')
async def create_new_user(user_data: UserCreate) -> UserGet:
    password = get_password_hash(user_data.password)
    user: User = await create_instance_by_kwargs(
        User,
        username=user_data.username,
        email=user_data.email,
        password=password.decode(),
        name=user_data.name,
        bio=user_data.bio
    )
    _ = await create_instance_by_kwargs(
        Moodboard,
        author=user,
        name=f"{user.username}'ын Хаотик",
        is_chaotic=True,
        is_private=True,
    )
    print(_)
    return user


@router.get('/user')
async def list_user(
    user: Annotated[User, Depends(is_authenticated)],
    paginator=Depends(pagination),
    search: str | None = None
) -> PaginatedUser:
    return await paginator(get_all_users(search), UserGet)


@router.post('/auth')
async def auth_user(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> str:
    user: User = await get_instance_or_404(User, username=user_data.username)
    if not bcrypt.checkpw(user_data.password.encode(), user.password.encode()):
        raise WrongLoginOrPassword
    token = create_access_token(
        data={'sub': user_data.username}
    )
    return token


@router.get('/user/me')
async def get_current_user(
    user: Annotated[User, Depends(is_authenticated)]
) -> UserGet:
    return user


@router.get('/user/{user_id}')
async def retrieve_user(user_id: int) -> UserGet:
    return await get_instance_or_404(User, id=user_id)


@router.post('/user/{user_id}/sub')
async def subscribe_on_user(
    user_id: int,
    user: Annotated[User, Depends(is_authenticated)]
):
    subscribed_for: User = await subscribe_on_user_db(user, user_id)
    return f'Успешно подписались на пользователя {subscribed_for.username}'


@router.delete('/user/{user_id}/sub')
async def unsubscribe_from_user(
    user_id: int,
    user: Annotated[User, Depends(is_authenticated)]
):
    await delete_user_from_subs(user, user_id)
    return 'Успешно отписались от пользователя'


@router.get('/sub')
async def list_subs(
    user: Annotated[User, Depends(is_authenticated)],
    paginator=Depends(pagination),
) -> PaginatedUser:
    return await paginator(get_user_subs(user), UserGet)
