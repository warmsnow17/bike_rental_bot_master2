import calendar
from datetime import datetime
from aiogram import types
from .base import SelectInlineKeyboard
from client_bot import helpers


class AdditionalParamsKeyboard(SelectInlineKeyboard):
    identifier: str = 'additional_params'

    def __init__(self, language: str):
        variants = [
            {'key': 'yes', 'value': helpers.language.get_translation(language, 'yes_button_label', 'Да')},
            {'key': 'no', 'value': helpers.language.get_translation(language, 'no_button_label', 'Нет')}
        ]
        super().__init__(variants)


class RequestABSSelectionKeyboard(SelectInlineKeyboard):
    identifier: str = 'request_abs_param'

    def __init__(self, language: str):
        variants = [
            {'key': 'yes', 'value': helpers.language.get_translation(language, 'yes_button_label', 'Да')},
            {'key': 'no', 'value': helpers.language.get_translation(language, 'no_button_label', 'Нет')},
            {'key': 'any', 'value': helpers.language.get_translation(language, 'any_button_label', 'Неважно')}
        ]
        super().__init__(variants)


class RequestKeylessSelectionKeyboard(SelectInlineKeyboard):
    identifier: str = 'request_keyless_param'

    def __init__(self, language: str):
        variants = [
            {'key': 'yes', 'value': helpers.language.get_translation(language, 'yes_button_label', 'Да')},
            {'key': 'no', 'value': helpers.language.get_translation(language, 'no_button_label', 'Нет')},
            {'key': 'any', 'value': helpers.language.get_translation(language, 'any_button_label', 'Неважно')}
        ]
        super().__init__(variants)


class RentTypeKeyboard(SelectInlineKeyboard):
    identifier: str = 'rent_type'

    def __init__(self, language: str):
        variants = [
            {'key': 'day', 'value': helpers.language.get_translation(language, 'day_button_label', 'Сутки')},
            {'key': 'week', 'value': helpers.language.get_translation(language, 'week_button_label', 'Неделя')},
            {'key': 'month', 'value': helpers.language.get_translation(language, 'month_button_label', 'Месяц')}
        ]
        super().__init__(variants)


class RequestYearKeyboard(SelectInlineKeyboard):
    identifier: str = 'rent_year_limit'

    def __init__(self, language: str, years: list = [2018, 2020, 2022, 2023]):
        variants = []
        i = 0
        for year in years:
            i += 1
            if i != len(years):
                variants.append(
                    {
                        'key': str(year),
                        'value': helpers.language.get_translation(language, 'year_from', 'От') + f' {year}'
                    }
                )
            else:
                variants.append(
                    {
                        'key': str(year),
                        'value': f'{year}'
                    }
                )
        variants.append({
            'key': 'any',
            'value': helpers.language.get_translation(language, 'any_button_label', 'Любой')
        })
        super().__init__(variants)


class RequestMileageKeyboard(SelectInlineKeyboard):
    identifier: str = 'rent_mileage_limit'

    def __init__(self, language: str, mileage: list = [1000, 5000, 10000, 15000]):
        variants = []
        for mileage in mileage:
            variants.append(
                {
                    'key': str(mileage),
                    'value': helpers.language.get_translation(language, 'mileage_to', 'До') + f' {mileage}'
                }
            )
        variants.append({
            'key': 'any',
            'value': helpers.language.get_translation(language, 'any_mileage_button_label', 'Любой')
        })
        super().__init__(variants)


class RequestColorSelectionKeyboard(SelectInlineKeyboard):
    identifier: str = 'request_select_bike_color'

    def __init__(self, language: str):
        variants = [
            {'key': 'bright', 'value': helpers.language.get_translation(language, 'bright_color_label', 'Яркий')},
            {'key': 'white', 'value': helpers.language.get_translation(language, 'white_color_label', 'Белый')},
            {'key': 'red', 'value': helpers.language.get_translation(language, 'red_color_label', 'Красный')},
            {'key': 'black', 'value': helpers.language.get_translation(language, 'black_color_label', 'Черный')},
            {'key': 'blue', 'value': helpers.language.get_translation(language, 'blue_color_label', 'Синий')},
            {'key': 'yellow', 'value': helpers.language.get_translation(language, 'yellow_color_label', 'Желтый')},
            {'key': 'any', 'value': helpers.language.get_translation(language, 'any_color_label', 'Любой')},
        ]
        super().__init__(variants)


class RequestRentTypeSelectKeyboard(SelectInlineKeyboard):
    identifier: str = 'request_rent_type_selection'

    def __init__(self, language: str):
        variants = [
            {'key': 'daily', 'value': helpers.language.get_translation(language, 'daily_rent_label', 'На один/несколько дней')},
            {'key': 'weekly', 'value': helpers.language.get_translation(language, 'weekly_rent_label', 'От недели до месяца')},
            {'key': 'monthly', 'value': helpers.language.get_translation(language, 'monthly_rent_label', 'Более месяца')},
        ]
        super().__init__(variants)


class RequestRentStartDateKeyboard:
    identificator: str = 'rent_start_date'

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


class NewBikeRentRequestKeyboard:
    
    def __init__(self, language: str, offer_id: int) -> None:
        self.language = language
        self.offer_id = offer_id

    def markup(self) -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton(
                helpers.language.get_translation(self.language, 'yes_button_label', 'yes'),
                callback_data=f'offer:confirm:{self.offer_id}'
            ),
            types.InlineKeyboardButton(
                helpers.language.get_translation(self.language, 'no_button_label', 'no'),
                callback_data=f'offer:cancel:{self.offer_id}'
            ),
        )
        return keyboard

    @classmethod
    def get_regexp(cls) -> str:
        return f'^offer:[\w]+:[\d]+$'


class AcceptOfferKeyboard:

    def __init__(self, language: str, offer_id: int):
        self.language = language
        self.offer_id = offer_id

    def markup(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton(
                helpers.language.get_translation(self.language, 'accept_offer', 'Хочу этот байк'),
                callback_data=f'offer:accept:{self.offer_id}'
            )
        )
        return keyboard

    @classmethod
    def get_regexp(cls) -> str:
        return f'^offer:[\w]+:[\d]+$'


class RequestCreatedKeyboard:

    rows = [
        ['rent_another_bike_button_label'],
        ['chat_with_manager_button_label'],
    ]

    def __init__(self, language: str) -> None:
        self.language = language

    @classmethod
    def get_button_id_by_text(cls, language: str, text: str) -> str:
        for row in cls.rows:
            button_id = row[0]
            button_text = helpers.language.get_translation(language, button_id, '')
            if button_text == text:
                return button_id
        return None

    def markup(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for row in self.rows:
            buttons = []
            for button_id in row:
                text = helpers.language.get_translation(self.language, button_id, button_id)
                buttons.append(types.KeyboardButton(text))
            keyboard.row(*buttons)
        return keyboard


class ChatWithManagerKeyboard:

    def __init__(self, language: str, manager: object):
        self.language = language
        self.manager = manager

    def markup(self) -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton(
                helpers.language.get_translation(
                    self.language,
                    'chat_with_manager_button_label',
                    'Чат с менеджером'
                ),
                url=f'https://t.me/{self.manager.username}'
            )
        )
        return keyboard


class ManagerOfferKeyboard:

    def __init__(self, language: str, offer_id: int):
        self.language = language
        self.offer_id = offer_id

    def markup(self):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(
            types.InlineKeyboardButton(
                helpers.language.get_translation(self.language, 'succcess_offer_button_label', 'Успешный'),
                callback_data=f'moffer:accept:{self.offer_id}'
            )
        )
        keyboard.row(
            types.InlineKeyboardButton(
                helpers.language.get_translation(self.language, 'fail_offer_button_label', 'Отменен'),
                callback_data=f'moffer:cancel:{self.offer_id}'
            )
        )
        return keyboard

    @classmethod
    def get_regexp(cls) -> str:
        return f'^moffer:[\w]+:[\d]+$'


class RequestHelmetsKeyboard(SelectInlineKeyboard):
    identifier: str = 'request_helmets_selection'

    def __init__(self, language: str):
        variants = [
            {'key': 'one', 'value': helpers.language.get_translation(language, 'one_helmet_label', 'Один шлем')},
            {'key': 'two', 'value': helpers.language.get_translation(language, 'two_helmets_label', 'Два шлема')},
            {'key': 'no', 'value': helpers.language.get_translation(language, 'no_helmets_label', 'Шлемы не нужны')},
        ]
        super().__init__(variants)


class ConfirmationKeyboard(SelectInlineKeyboard):
    identifier: str = 'request_confirmation_selection'

    def __init__(self, language: str):
        variants = [
            {'key': 'confirm', 'value': helpers.language.get_translation(language, 'confirm_button_label', 'Подтверждаю')},
        ]
        super().__init__(variants)
