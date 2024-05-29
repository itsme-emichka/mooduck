from tortoise import Model, fields


class Comment(Model):
    id = fields.BigIntField(pk=True)
    author = fields.ForeignKeyField(
        'models.User',
        related_name='comment'
    )
    moodboard = fields.ForeignKeyField(
        'models.Moodboard',
        related_name='comment'
    )
    answering_to = fields.ForeignKeyField(
        'models.Comment',
        related_name='comment',
        null=True
    )
    text = fields.CharField(max_length=2048)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)


class Like(Model):
    id = fields.BigIntField(pk=True)
    author = fields.ForeignKeyField(
        'models.User',
        related_name='like'
    )
    moodboard = fields.ForeignKeyField(
        'models.Moodboard',
        related_name='like'
    )
    created_at = fields.DatetimeField(auto_now_add=True)
