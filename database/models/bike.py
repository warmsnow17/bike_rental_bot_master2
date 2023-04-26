import typing
from datetime import datetime, timedelta
from tortoise import fields
from .base import TimedBaseModel
from .request import RentalRequest, BikeOffer
from .option import Option


class BikeModel(TimedBaseModel):
    name = fields.CharField(max_length=255)

    async def has_available_bikes(self, date) -> bool:
        not_available_bike_ids = await BikeBooking.filter(from_date__lte=date, to_date__gte=date).values_list('bike_id', flat=True)
        total_bikes = await self.bikes.all().exclude(id__in=not_available_bike_ids).count()
        return total_bikes > 0

    async def get_lowes_price(self) -> float:
        cheapes_bike = await self.bikes.all().order_by('monthly_price').first()
        if cheapes_bike:
            return cheapes_bike.monthly_price / 30
        return 0.0


class Bike(TimedBaseModel):
    user = fields.ForeignKeyField('models.User', related_name='bikes')
    model = fields.ForeignKeyField('models.BikeModel', related_name='bikes')
    year = fields.IntField()
    mileage = fields.IntField()
    color = fields.CharField(max_length=255)
    abs = fields.BooleanField()
    keyless = fields.BooleanField()
    number = fields.CharField(max_length=100)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    weekly_price = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    biweekly_price = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    threeweekly_price = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    monthly_price = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    bimonthly_price = fields.DecimalField(max_digits=10, decimal_places=2, default=0)
    rental_start_date = fields.DatetimeField(null=True)

    @classmethod
    async def get_for_request(cls, request: RentalRequest) -> list['Bike']:
        queryset = Bike.filter(
            model=request.model
        ).filter(
            rental_start_date__lte=request.rent_start_date
        ).select_related('user', 'model')
        
        busy_bike_ids = await BikeBooking.filter(
            from_date__lte=request.rent_end_date,
            to_date__gte=request.rent_start_date
        ).values_list('bike_id', flat=True)
        queryset = queryset.exclude(id__in=busy_bike_ids)
        if request.additional_params:
            if request.year_from > 0:
                queryset = queryset.filter(year__gte=request.year_from)
            if request.color != 'any':
                queryset = queryset.filter(color=request.color)
            if request.abs in ('yes', 'no'):
                queryset = queryset.filter(abs=request.abs == 'yes')
            if request.keyless in ('yes', 'no'):
                queryset = queryset.filter(keyless=request.keyless == 'yes')
        return await queryset.all()

    async def get_bike_status(self):
        last_offer = await BikeOffer.filter(bike=self).select_related('request').order_by('-id').first()
        if not last_offer:
            return 'Free'
        if last_offer.status == BikeOffer.OfferStatuses.ACCEPTED:
            return 'Manager'
        if last_offer.status == BikeOffer.OfferStatuses.NEW:
            option = await Option.filter(key='bike_request_lifetime').first()
            if not option:
                request_lifetime = 5
            else:
                try:
                    request_lifetime = int(option.value)
                except:
                    request_lifetime = 5
            offer_date = datetime.now() - timedelta(minutes=int(request_lifetime))
            if last_offer.request.created_at < offer_date.astimezone():
                return 'Rental'
            else:
                return 'New'
        if last_offer.status == BikeOffer.OfferStatuses.EXPIRED:
            return 'Rental'
        if last_offer.status == BikeOffer.OfferStatuses.COMPLETE:
            if last_offer.request.rent_start_date < datetime.now().astimezone() and last_offer.request.rent_end_date > datetime.now().astimezone():
                return 'In rent'
            else:
                return 'Free'
        return 'Free'

    def __str__(self):
        return f'{self.model.name} - {self.number}'


class BikePhoto(TimedBaseModel):
    bike = fields.ForeignKeyField('models.Bike', related_name='photos')
    telegram_id = fields.CharField(max_length=255)
    file = fields.CharField(max_length=255, default='')


class BikeBooking(TimedBaseModel):
    bike = fields.ForeignKeyField('models.Bike', related_name='bookings')
    offer = fields.ForeignKeyField('models.BikeOffer', related_name='booking')
    from_date = fields.DatetimeField()
    to_date = fields.DatetimeField()
