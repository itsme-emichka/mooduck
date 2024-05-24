from tortoise.queryset import QuerySetSingle
from tortoise import Model
from tortoise.exceptions import IntegrityError
from fastapi import HTTPException, status


async def get_instance_or_404(
        model: Model,
        **kwargs
) -> QuerySetSingle:
    instance = await model.get_or_none(**kwargs)
    if not instance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='сущность не найдена'
        )
    return instance


async def create_instance_by_kwargs(model: Model, **kwargs) -> QuerySetSingle:
    try:
        return await model.create(**kwargs)
    except IntegrityError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ex
        )
