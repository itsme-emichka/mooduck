from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import jwt, JWTError

from config import SECRET_KEY, ALGORITHM
from extra.services import get_instance_or_404
from users.models import User


oauth = OAuth2PasswordBearer(tokenUrl='token')


async def is_authenticated(token: Annotated[str, Depends(oauth)]) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if not username:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)
    return await get_instance_or_404(User, username=username)
