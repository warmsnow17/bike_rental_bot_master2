from typing import Optional
from starlette.requests import Request
from fastapi_admin.resources import ComputeField, displays, Widget
from database.models import RentalRequest


class CoordinatesField(ComputeField):

    async def get_value(self, request: Request, obj: dict):
        lat = obj.get('lat')
        lon = obj.get('lon')
        return f'{lat} {lon}'


class ComputedForeignKeyField(ComputeField):

    def __init__(self, name: str, model, label: Optional[str] = None, display: Optional[displays.Display] = None, input_: Optional[Widget] = None):
        self.model = model
        super().__init__(name, label, display, input_)

    async def get_value(self, request: Request, obj: dict):
        related_obj_id = obj.get(f'{self.name}_id')
        if not related_obj_id:
            return ''
        f_obj = await self.model.get_or_none(pk=related_obj_id)
        if f_obj:
            return str(f_obj)
        return '-'


class ComputedForeignKeyFieldValueField(ComputeField):

    def __init__(self, name: str, model, field: str, label: Optional[str] = None, display: Optional[displays.Display] = None, input_: Optional[Widget] = None):
        self.model = model
        self.field = field
        super().__init__(name, label, display, input_)

    async def get_value(self, request: Request, obj: dict):
        related_obj_id = obj.get(f'{self.name}_id')
        if not related_obj_id:
            return ''
        f_obj = await self.model.get_or_none(pk=related_obj_id)
        if f_obj:
            return getattr(f_obj, self.field, '-')
        return '-'


class ComputedSelectedOfferBikeField(ComputeField):

    def __init__(self, name: str, model, label: Optional[str] = None, display: Optional[displays.Display] = None, input_: Optional[Widget] = None):
        self.model = model
        super().__init__(name, label, display, input_)

    async def get_value(self, request: Request, obj: dict):
        related_obj_id = obj.get(f'{self.name}_id')
        if not related_obj_id:
            return '-'
        f_obj = await self.model.get_or_none(pk=related_obj_id).select_related('bike', 'bike__model')
        if f_obj:
            return str(f_obj.bike)
        return '-'


class ComputedSelectedOfferBikeOwnerField(ComputeField):

    def __init__(self, name: str, model, label: Optional[str] = None, display: Optional[displays.Display] = None, input_: Optional[Widget] = None):
        self.model = model
        super().__init__(name, label, display, input_)

    async def get_value(self, request: Request, obj: dict):
        related_obj_id = obj.get(f'{self.name}_id')
        if not related_obj_id:
            return '-'
        f_obj = await self.model.get_or_none(pk=related_obj_id).select_related('bike__user')
        if f_obj:
            return f_obj.bike.user.username
        return '-'


class ComputedRequestStatusField(ComputeField):

    async def get_value(self, request: Request, obj: dict):
        if obj.get('status') == RentalRequest.RequestStatuses.NEW:
            return 'Новый'
        if obj.get('status') == RentalRequest.RequestStatuses.CANCELED:
            return 'Отменен'
        if obj.get('status') == RentalRequest.RequestStatuses.SELECTED:
            return 'У менеджера'
        if obj.get('status') == RentalRequest.RequestStatuses.COMPLETE:
            return 'Подтвержден'


class ComputedSettingNameField(ComputeField):

    KNOWN_SETTINGS = {
        'idr_per_usd_exchange_rate': 'USD/IDR курс',
        'bike_request_lifetime': 'Время на ответ поставщика(минуты)',
        'max_confirmed_offers': 'Количество предложений в выдаче',
        'fee_percent': 'Процент комиссии',

    }

    async def get_value(self, request: Request, obj: dict):
        key = obj.get('key')
        return ComputedSettingNameField.KNOWN_SETTINGS.get(key)
