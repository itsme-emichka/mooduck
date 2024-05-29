from tortoise import Model, fields

from items.validators import ChoicesValidator


ITEM_TYPES: dict[str, str] = {
    'anime': 'Аниме',
    'movie': 'Кино',
    'series': 'Сериал',
    'video': 'Видео',
    'state': 'Статья',
    'image': 'Картинка',
    'site': 'Сайт',
    'gif': 'Гифка',
    'music': 'Музыка',
    'game': 'Игра',
    'book': 'Книга',
    'site': 'Сайт'
}

MEDIA_TYPES: list[str] = [
    'image',
    'gif',
    'video',
]


class ItemMoodboard(Model):
    id = fields.BigIntField(pk=True)
    item = fields.ForeignKeyField(
        'models.Item',
        related_name='item_moodboard'
    )
    moodboard = fields.ForeignKeyField(
        'models.Moodboard',
        related_name='item_moodboard'
    )


class Item(Model):
    id = fields.BigIntField(pk=True)
    author = fields.ForeignKeyField('models.User', related_name='item')
    name = fields.CharField(max_length=512)
    description = fields.TextField(null=True)
    item_type = fields.CharField(
        max_length=128,
        validators=[ChoicesValidator(ITEM_TYPES.keys())]
    )
    link = fields.CharField(max_length=1024, null=True)
    media = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', 'name']
