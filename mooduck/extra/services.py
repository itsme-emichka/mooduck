from tortoise.queryset import QuerySetSingle, QuerySet
from tortoise import Model
from tortoise.exceptions import IntegrityError

from extra.exceptions import NotFound, AlreadyExists


async def get_instance_or_404(
        model: Model,
        **kwargs
) -> QuerySetSingle:
    instance = await model.get_or_none(**kwargs)
    if not instance:
        raise NotFound
    return instance


async def create_instance_by_kwargs(model: Model, **kwargs) -> QuerySetSingle:
    try:
        return await model.create(**kwargs)
    except IntegrityError as ex:
        print(ex)
        raise AlreadyExists


async def paginate_queryset(
    queryset: QuerySet,
    limit: int = 50,
    offset: int = 0
) -> list[Model]:
    return await queryset.limit(limit).offset(offset)
