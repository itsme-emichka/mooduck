from typing import Any
from tortoise.validators import Validator
from tortoise.exceptions import ValidationError


class ChoicesValidator(Validator):
    def __init__(self, choices: list[Any]) -> None:
        self.choices = choices

    def __call__(self, value: Any):
        if value not in self.choices:
            raise ValidationError('Value is not in available choices')
