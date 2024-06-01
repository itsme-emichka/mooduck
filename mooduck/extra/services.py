from tortoise.queryset import QuerySetSingle, QuerySet
from tortoise import Model
from tortoise.exceptions import IntegrityError
from fastapi import HTTPException, status


async def get_instance_or_404(
        model: Model,
        **kwargs
) -> QuerySetSingle:
    instance = await model.get_or_none(**kwargs)
    if not instance:
        raise HTTPException(404)
    return instance


async def create_instance_by_kwargs(model: Model, **kwargs) -> QuerySetSingle:
    try:
        return await model.create(**kwargs)
    except IntegrityError as ex:
        print(ex)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Already exists'
        )


async def paginate_queryset(
    queryset: QuerySet,
    limit: int = 50,
    offset: int = 0
) -> list[Model]:
    return await queryset.limit(limit).offset(offset)
