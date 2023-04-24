import typing
from tortoise import fields
from .base import TimedBaseModel


class Garage(TimedBaseModel):
    owner = fields.ForeignKeyField('models.User', related_name='garages')
    name = fields.TextField(max_lendth=255)
    owner_name = fields.TextField(max_length=255)
    lat = fields.FloatField()
    lon = fields.FloatField()
