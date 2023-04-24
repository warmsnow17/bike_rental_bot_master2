import typing
from tortoise import fields
from .base import BaseModel


class ReplyMessage(BaseModel):
    action = fields.TextField(max_length=255)
    language = fields.TextField(max_length=3)
    message = fields.TextField()

    class Meta:
        unique_together = ('action', 'language')

    @classmethod
    async def get_for_language(cls, language: str) -> typing.Optional['ReplyMessage']:
        return await cls.filter(language=language)
