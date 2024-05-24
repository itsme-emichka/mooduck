from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
import bcrypt

from users.schemas import UserCreate, UserGet
from users.models import User
from extra.services import (create_instance_by_kwargs, get_instance_or_404)
from extra.utils import get_password_hash, create_access_token
from extra.dependencies import is_authenticated


router = APIRouter()
oauth_scheme = OAuth2PasswordBearer('token', auto_error=True)


@router.post('/users')
async def create_new_user(user_data: UserCreate) -> UserGet:
    password = get_password_hash(user_data.password)
    user = await create_instance_by_kwargs(
        User,
        username=user_data.username,
        email=user_data.email,
        password=password.decode(),
        name=user_data.name,
    )
    return user


@router.get('/users')
async def users_list() -> list[UserGet]:
    return await User.all()


@router.delete('/users/{id}')
async def delete_user(id: int):
    return await User.get_or_none(id=id).delete()


@router.post('/auth')
async def auth_user(user_data: UserCreate) -> str:
    user: User = await get_instance_or_404(User, username=user_data.username)
    if not bcrypt.checkpw(user_data.password.encode(), user.password.encode()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Неверный логин или пароль'
        )
    token = create_access_token(
        data={'sub': user_data.username}
    )
    return token


@router.get('/users/me')
async def get_current_user(
    user: Annotated[User, Depends(is_authenticated)]
) -> UserGet:
    return user
