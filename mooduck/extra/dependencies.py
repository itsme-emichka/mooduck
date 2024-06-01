from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, Request, Query
from jose import jwt, JWTError
from tortoise.queryset import QuerySet
from pydantic import BaseModel

from config import SECRET_KEY, ALGORITHM
from extra.services import get_instance_or_404, paginate_queryset
from extra.schemas import Pagination
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


async def pagination(
    request: Request,
    limit: Annotated[int, Query(ge=1)] = 30,
    page: Annotated[int, Query(ge=1)] = 1,
):
    base_url = str(request.base_url)[:-1]
    path = str(request.url.path)
    query = str(request.url.remove_query_params(('limit', 'page')).query)

    url = f'{base_url}{path}'

    async def get_paginated_response(queryset: QuerySet, schema: BaseModel):
        prev_page = f'{url}?limit={limit}&page={page - 1}&{query}'
        if page == 1:
            prev_page = None
        next_page = None

        items = await paginate_queryset(
            queryset=queryset,
            limit=limit + 1,
            offset=((page - 1) * limit)
        )

        if len(items) > limit:
            next_page = f'{url}?limit={limit}&page={page + 1}&{query}'
            items = items[:-1]

        return Pagination(
            page=page,
            limit=limit,
            prev_page=prev_page,
            next_page=next_page,
            amount=len(items),
            items=[schema.model_validate(item) for item in items]
        )
    return get_paginated_response
