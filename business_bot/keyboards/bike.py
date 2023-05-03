import calendar
import math
from tortoise.queryset import QuerySet
from datetime import datetime
from aiogram import types
from business_bot import helpers
from database.models import Bike
from .base import SelectObjectKeyboard, SelectInlineKeyboard


class SelectBikeModelKeyboard(SelectObjectKeyboard):
    identifier: str = 'select_bike_model'


class SelectBikeColorKeyboard(SelectInlineKeyboard):
    identifier: str = 'select_bike_color'


class SelectBikeAbsKeyboard(SelectInlineKeyboard):
    identifier: str = 'select_bike_abs'

    def __init__(self, language: str):
        variants = [
            {'key': 'yes', 'value': helpers.language.get_translation(language, 'yes_button_label', 'Да')},
            {'key': 'no', 'value': helpers.language.get_translation(language, 'no_button_label', 'Нет')}
        ]
        super().__init__(variants)


class SelectBikeKeylessKeyboard(SelectInlineKeyboard):
    identifier: str = 'select_bike_keyless'

    def __init__(self, language: str):
        variants = [
            {'key': 'yes', 'value': helpers.language.get_translation(language, 'yes_button_label', 'Да')},
            {'key': 'no', 'value': helpers.language.get_translation(language, 'no_button_label', 'Нет')}
        ]
        super().__init__(variants)


class BikeConfirmationKeyboard(SelectInlineKeyboard):
    identifier: str = 'review_bike'

    def __init__(self, language: str):
        variants = [
            {'key': 'yes', 'value': helpers.language.get_translation(language, 'yes_button_label', 'Да')},
            {'key': 'no', 'value': helpers.language.get_translation(language, 'no_button_label', 'Нет')}
        ]
        super().__init__(variants)


class BikeAvailabilityKeyboard:
    identificator: str = 'availability'

    def __init__(self, language: str, month: int = None, year: int = None) -> None:
        self.current_date = datetime.now()
        self.language = language
        self.month = month if month is not None else self.current_date.month
        self.year = year if year is not None else self.current_date.year

    def markup(self) -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup(row_width=7)
        month_name = helpers.language.get_translation(self.language, f'month_{self.month:02d}', f'{self.month:02d}')
        keyboard.row(
            types.InlineKeyboardButton('<<', callback_data=f'{self.identificator}:sw:{self.year}:{self.month-1}:n'),
            types.InlineKeyboardButton(f'{month_name}', callback_data='{self.identificator}:ig:n:n'),
            types.InlineKeyboardButton('>>', callback_data=f'{self.identificator}:sw:{self.year}:{self.month+1}:n'),
        )
        keyboard.row(
            types.InlineKeyboardButton('<<', callback_data=f'{self.identificator}:sw:{self.year-1}:{self.month}:n'),
            types.InlineKeyboardButton(f'{self.year}', callback_data='{self.identificator}:ig:n:n'),
            types.InlineKeyboardButton('>>', callback_data=f'{self.identificator}:sw:{self.year+1}:{self.month}:n'),
        )
        keyboard.row()
        for day in ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']:
            week_day = helpers.language.get_translation(self.language, f'week_{day.lower()}', day)
            keyboard.insert(
                types.InlineKeyboardButton(week_day, callback_data=f'{self.identificator}:ig:n:n:n')
            )
        month_calendar = calendar.monthcalendar(self.year, self.month)
        for week in month_calendar:
            keyboard.row()
            for day in week:
                if day == 0:
                    keyboard.insert(
                        types.InlineKeyboardButton(
                            ' ',
                            callback_data=f'{self.identificator}:ig:n:n'
                        )
                    )
                else:
                    day_text = str(day)
                    if self.year == self.current_date.year and self.month == self.current_date.month and day == self.current_date.day:
                        day_text = f'[{day}]'
                    keyboard.insert(
                        types.InlineKeyboardButton(
                            day_text,
                            callback_data=f'{self.identificator}:sl:{self.year}:{self.month}:{day}'
                        )
                    )
        return keyboard

    @classmethod
    def get_regexp(cls) -> str:
        return f'^{cls.identificator}:[\w]+:[\d\w]+:[\d\w]+:[\d\w]+$'


class MyBikesKeyboard:
    identifier: str = 'mybikes'

    def __init__(self, queryset: QuerySet, language: str, page: int = 1, per_page: int = 10, add_back_button: bool = False) -> None:
        self.queryset = queryset
        self.language = language
        self.page = page
        self.per_page = per_page
        self.add_back_button = add_back_button

    async def markup(self) -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup()
        offset = (self.page - 1) * self.per_page
        limit = self.per_page
        items = await self.queryset.all().select_related('model').offset(offset).limit(limit)
        total_pages = math.ceil(await self.queryset.all().count() / self.per_page)
        for bike in items:
            keyboard.row(
                types.InlineKeyboardButton(
                    f'{bike.model.name} - {bike.number}',
                    callback_data=f'{self.identifier}:sl:{bike.pk}'
                )
            )

        if total_pages > 1:
            keyboard.row()
            if self.page > 1:
                keyboard.insert(
                    types.InlineKeyboardButton(
                        '<',
                        callback_data=f'{self.identifier}:pg:{self.page - 1}'
                    )
                )
            else:
                keyboard.insert(
                    types.InlineKeyboardButton(
                        ' ',
                        callback_data=f'{self.identifier}:ig:n'
                    )
                )
            keyboard.insert(
                types.InlineKeyboardButton(
                    str(self.page),
                    callback_data=f'{self.identifier}:ig:n'
                )
            )
            if self.page < total_pages:
                keyboard.insert(
                    types.InlineKeyboardButton(
                        '>',
                        callback_data=f'{self.identifier}:pg:{self.page + 1}'
                    )
                )
            else:
                keyboard.insert(
                    types.InlineKeyboardButton(
                        ' ',
                        callback_data=f'{self.identifier}:ig:n'
                    )
                )
        if self.add_back_button:
            keyboard.row(
                types.InlineKeyboardButton(
                    helpers.language.get_translation(self.language, 'back_button_label', 'Назад'),
                    callback_data=f'{self.identifier}:bk:n'
                )
            )
        return keyboard

    @classmethod
    def get_regexp(cls) -> str:
        return f'^{cls.identifier}:[\w\d]+:[\w\d]+$'


class RentBikesKeyboard(MyBikesKeyboard):
    identifier: str = 'rent_bikes_keyboard'


class AvailableBikesKeyboard(MyBikesKeyboard):
    identifier: str = 'available_bikes_keyboard'


class BikeManagementKeyboard:

    def __init__(self, language: str, bike: Bike) -> None:
        self.bike = bike
        self.language = language

    def markup(self) -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.row(
            types.InlineKeyboardButton(
                helpers.language.get_translation(self.language, 'set_bike_availability_button_label', 'Указать дату старта'),
                callback_data=f'bike:date:{self.bike.pk}'
            )
        )
        keyboard.row(
            types.InlineKeyboardButton(
                helpers.language.get_translation(self.language, 'edit_bike_button_label', 'Редактировать байк'),
                callback_data=f'bike:edit:{self.bike.pk}'
            )
        )
        keyboard.row(
            types.InlineKeyboardButton(
                helpers.language.get_translation(self.language, 'delete_bike_button_label', 'Удалить байк'),
                callback_data=f'bike:delete:{self.bike.pk}'
            )
        )
        keyboard.row(
            types.InlineKeyboardButton(
                helpers.language.get_translation(self.language, 'back_button_label', 'Назад'),
                callback_data=f'bike:list:0'
            )
        )
        return keyboard

    @classmethod
    def get_regexp(cls) -> str:
        return '^bike:[\w]+:[\d]+$'


class ConfirmBikeDeletionKeyboard:

    def __init__(self, language: str, bike_id: int) -> None:
        self.language = language
        self.bike_id = bike_id

    def markup(self) -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton(
                helpers.language.get_translation(self.language, 'yes_button_label', 'Да'),
                callback_data=f'bikedeletion:confirm:{self.bike_id}'
            )
        )
        keyboard.row(
            types.InlineKeyboardButton(
                helpers.language.get_translation(self.language, 'no_button_label', 'Нет'),
                callback_data=f'bikedeletion:cancel:{self.bike_id}'
            )
        )
        return keyboard

    @classmethod
    def get_regexp(cls) -> str:
        return '^bikedeletion:[\w]+:[\d]+$'


class GarageBikesKeyboard(SelectInlineKeyboard):
    identifier: str = 'garage_bikes'

    def __init__(self, language: str):
        variants = [
            {'key': 'rent', 'value': helpers.language.get_translation(language, 'bikes_in_rent_button_label', 'В аренде')},
            {'key': 'available', 'value': helpers.language.get_translation(language, 'available_bikes_button_label', 'Свободные байки')},
        ]
        super().__init__(variants)
