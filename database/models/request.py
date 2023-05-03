from enum import IntEnum
from tortoise import fields
from tortoise.expressions import Q
from .base import TimedBaseModel


class RentalRequest(TimedBaseModel):
    class Meta:
        ordering = ['-created_at']

    class RequestStatuses(IntEnum):
        NEW = 0
        CANCELED = 1
        SELECTED = 2
        COMPLETE = 3
    status = fields.IntEnumField(RequestStatuses, default=RequestStatuses.NEW)
    manager = fields.ForeignKeyField('models.User', related_name='managed_requests', null=True)
    user = fields.ForeignKeyField('models.User', related_name='created_requests')
    model = fields.ForeignKeyField('models.BikeModel', related_name='user_requests')
    additional_params = fields.BooleanField()
    year_from = fields.IntField()
    mileage_to = fields.IntField()
    helmets = fields.CharField(max_length=255, default='')
    lat = fields.FloatField(default=0)
    lon = fields.FloatField(default=0)
    color = fields.CharField(max_length=255)
    abs = fields.CharField(max_length=255)
    keyless = fields.CharField(max_length=255)
    rent_type = fields.CharField(max_length=255)
    rent_amount = fields.IntField()
    rent_start_date = fields.DatetimeField()
    rent_end_date = fields.DatetimeField(null=True)
    selected_offer = fields.ForeignKeyField('models.BikeOffer', null=True)

    @property
    def created_at_date(self):
        return self.created_at.date()


class BikeOffer(TimedBaseModel):
    class OfferStatuses(IntEnum):
        NEW = 0
        ACCEPTED = 1
        REJECTED = 2
        CONFIRMED = 3
        COMPLETE = 4
        EXPIRED = 5
    status = fields.IntEnumField(OfferStatuses, default=OfferStatuses.NEW)
    client = fields.ForeignKeyField('models.User')
    business_message_id = fields.CharField(max_length=255, default='')
    client_message_id = fields.CharField(max_length=255, default='')
    request = fields.ForeignKeyField('models.RentalRequest', related_name='offers')
    bike = fields.ForeignKeyField('models.Bike')
    price = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_with_fee = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_sum = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_sum_with_fee = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
