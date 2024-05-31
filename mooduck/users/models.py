import re

from tortoise.models import Model
from tortoise import fields
from tortoise.validators import RegexValidator

from config import SLUG_PATTERN, EMAIL_PATTERN, ROLE_CHOICES_PATTERN


class User(Model):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(
        max_length=128,
        validators=[RegexValidator(SLUG_PATTERN, re.A)],
        unique=True,
    )
    password = fields.CharField(max_length=128)
    email = fields.CharField(
        max_length=512,
        validators=[RegexValidator(EMAIL_PATTERN, re.A)],
        unique=True,
    )
    name = fields.CharField(
        max_length=512,
        null=True,
        unique=True,
    )
    role = fields.CharField(
        max_length=10,
        validators=[RegexValidator(ROLE_CHOICES_PATTERN, re.A)],
        default='user',
    )
    bio = fields.TextField(null=True)

    async def get_liked_moodboard_ids(self):
        return await self.all(
        ).select_related(
            'like'
        ).filter(
            like__author=self
        ).values_list('like__moodboard_id', flat=True)

    async def is_moodboard_liked(self, moodboard_id: int) -> bool:
        return moodboard_id in await self.get_liked_moodboard_ids()

    def __str__(self) -> str:
        return self.username


class Subscription(Model):
    id = fields.BigIntField(pk=True)
    subscriber = fields.ForeignKeyField(
        'models.User',
        related_name='subscriber'
    )
    subscribed_for = fields.ForeignKeyField(
        'models.User',
        related_name='subscribed_for'
    )
