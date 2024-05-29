from tortoise import Model, fields


class Moodboard(Model):
    id = fields.BigIntField(pk=True)
    author = fields.ForeignKeyField('models.User', related_name='moodboard')
    name = fields.CharField(max_length=512)
    description = fields.TextField(null=True)
    cover = fields.CharField(max_length=1024, null=True)
    is_private = fields.BooleanField(default=False)
    is_chaotic = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at', 'name']


class FavMoodboard(Model):
    id = fields.BigIntField(pk=True)
    user = fields.ForeignKeyField(
        'models.User',
        related_name='fav_moodboard'
    )
    moodboard = fields.ForeignKeyField(
        'models.Moodboard',
        related_name='fav_moodboard'
    )
