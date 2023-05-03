import typing
import random
import hashlib
import string
from enum import IntEnum
from tortoise import fields
from tortoise.contrib.postgres.functions import Random
from .base import TimedBaseModel


class User(TimedBaseModel):
    id = fields.BigIntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)
    username = fields.CharField(max_length=255, index=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    language = fields.CharField(max_length=3)
    active = fields.BooleanField(default=True)
    is_client = fields.BooleanField(default=False)
    is_business = fields.BooleanField(default=False)
    is_manager = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)
    password = fields.CharField(max_length=255, default='')

    @classmethod
    async def get_by_telegram_id_or_create(cls, telegram_id: int, username: str, first_name: str, last_name: str, language: str):
        user = await cls.get_or_none(telegram_id=telegram_id)
        created = False
        if not user:
            user = await User.create(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                language=language
            )
            created = True
        return user, created

    @classmethod
    async def get_by_id(cls, id: int) -> typing.Optional['User']:
        return await User.get_or_none(pk=id)

    async def has_garages(self) -> bool:
        return (await self.garages.all().count()) > 0

    @classmethod
    async def get_random_manager(cls) -> typing.Optional['User']:
        managers = await User.filter(is_manager=True).annotate(order=Random()).order_by('order')
        if len(managers) == 0:
            return None
        return managers[0]

    def __str__(self) -> str:
        return self.username
