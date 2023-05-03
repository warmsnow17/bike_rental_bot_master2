from enum import Enum
from typing import List, Tuple
from starlette.requests import Request
from fastapi_admin.app import app
from fastapi_admin.resources import Field, Link, Model, inputs, ToolbarAction, Action
from fastapi_admin.widgets import displays, filters, inputs
from fastapi_admin.enums import Method
from fastapi_admin.i18n import _
from database.models import User, Garage, RentalRequest, BikeOffer, Option, BikeModel
from .fields import (
    CoordinatesField, ComputedForeignKeyField, ComputedSelectedOfferBikeField,
    ComputedRequestStatusField, ComputedForeignKeyFieldValueField,
    ComputedSettingNameField, ComputedSelectedOfferBikeOwnerField
)


@app.register
class DashboardResource(Link):
    label = 'Главная'
    icon = 'fas fa-home'
    url = '/administrator'


@app.register
class DashboardResource(Link):
    label = 'Байки'
    url = '/administrator/bikes/export'


@app.register
class BikeModelResourcce(Model):
    label = 'Модели'
    model = BikeModel
    fields = [
        'id',
        'name'
    ]


class LanguageEnum(Enum):
    RUSSIAN = 'ru'
    ENGLISH = 'en'
    INDONESIAN = 'id'


@app.register
class UserResource(Model):
    label = 'Пользователи'
    model = User
    icon = 'fas fa-user'
    filters = [
        filters.Search(
            name='username',
            label='Имя пользователя',
            search_mode='equal',
            placeholder='Поиск по имени пользователя',
        )
    ]
    fields = [
        'id',
        Field(
            name='telegram_id',
            label='ID пользователя телеграм'
        ),
        Field(
            name='username',
            label='Имя пользователя телеграм'
        ),
        Field(
            name='first_name',
            label='Имя'
        ),
        Field(
            name='last_name',
            label='Фамилия'
        ),
        Field(
            name='language',
            label='Язык'
        ),
        Field(
            name='active',
            label='Активен',
            input_=inputs.Switch()
        ),
        Field(
            name='is_client',
            label='Клиент',
            input_=inputs.Switch()
        ),
        Field(
            name='is_business',
            label='Поставщик',
            input_=inputs.Switch()
        ),
        Field(
            name='is_manager',
            label='Менеджер',
            input_=inputs.Switch()
        )
    ]


@app.register
class GarageResource(Model):
    label = 'Гаражи'
    model = Garage
    icon = 'fas fa-garage'
    filters = [

    ]
    fields = [
        'id',
        ComputedForeignKeyField(
            name='owner',
            model=User,
            label='Владелец'
        ),
        Field(
            name='owner_id',
            label='Владелец',
            display=displays.InputOnly(),
            input_=inputs.ForeignKey(User)
        ),
        CoordinatesField(
            'coordinates',
            label='Координаты'
        ),
        Field(
            name='lat',
            display=displays.InputOnly(),
            label='Широта'
        ),
        Field(
            name='lon',
            display=displays.InputOnly(),
            label='Долгота'
        )
    ]


@app.register
class RentalRequestResource(Model):
    label = 'Запросы на аренду'
    model = RentalRequest
    icon = 'fas fa-garage'
    page_size = 100
    filters = [
        filters.Search(
            name='pk',
            label='ID заявки',
            search_mode='equal',
            placeholder='Поиск заявки по номеру',
        )

    ]

    fields = [
        'id',
        ComputedForeignKeyField(
            name='user',
            model=User,
            label='Пользователь',
            display=displays.Display(),
        ),
        ComputedSelectedOfferBikeField(
            name='selected_offer',
            model=BikeOffer,
            label='Байк',
            display=displays.Display(),
        ),
        ComputedSelectedOfferBikeOwnerField(
            name='selected_offer',
            model=BikeOffer,
            label='Поставщик',
            display=displays.Display(),
        ),
        ComputedRequestStatusField(
            name='status',
            label='Статус',
        ),
        ComputedForeignKeyField(
            name='manager',
            model=User,
            label='Менеджер',
            display=displays.Display(),
        ),
        Field(
            name='rent_type',
            label='Вид аренды',
            display=displays.Display(),
        ),
        Field(
            'rent_amount',
            label='Количество',
            display=displays.Display(),
        ),
        Field(
            name='created_at',
            label='Дата поступления',
            display=displays.DateDisplay(),
        ),
        Field(
            name='rent_start_date',
            label='Дата начала',
            display=displays.DateDisplay(),
        ),
        Field(
            name='rent_end_date',
            label='Дата завершения',
            display=displays.DateDisplay(),
        ),
        ComputedForeignKeyFieldValueField(
            name='selected_offer',
            model=BikeOffer,
            field='price',
            label='Цена',
        ),
        ComputedForeignKeyFieldValueField(
            name='selected_offer',
            model=BikeOffer,
            field='total_sum',
            label='Сумма',
        ),
    ]


    async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
        return [
        ]

    async def get_actions(self, request: Request) -> List[Action]:
        return [
        ]

    async def get_bulk_actions(self, request: Request) -> List[Action]:
        return [
        ]


@app.register
class OptionsResource(Model):
    label = 'Настройки'
    model = Option
    icon = 'fas fa-settings'
    filters = [
    ]
    fields = [
        'id',
        ComputedSettingNameField(
            name='key',
            label='Название'
        ),
        Field(
            name='key',
            label='Системное название',
            display=displays.InputOnly()
        ),
        Field(
            name='value',
            label='Значение'
        ),
    ]

    async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
        return [
        ]

    async def get_actions(self, request: Request) -> List[Action]:
        return [
            Action(
                label=_("update"), icon="ti ti-edit", name="update", method=Method.GET, ajax=False
            )
        ]

    async def get_bulk_actions(self, request: Request) -> List[Action]:
        return [
        ]