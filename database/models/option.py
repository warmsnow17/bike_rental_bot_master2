import typing
from tortoise import fields
from .base import BaseModel


class Option(BaseModel):
    key = fields.CharField(max_length=255)
    option_type = fields.CharField(max_length=100, default='')
    value = fields.CharField(max_length=255)

    @classmethod
    async def get_by_key(cls, key: str) -> typing.Optional['Option']:
        return await cls.get_or_none(key=key)
