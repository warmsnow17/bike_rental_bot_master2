from aiogram import types
from business_bot import helpers


class SelectInlineKeyboard:
    identifier: str = 'select_keyboard'

    def __init__(self, variants: list, id_key: str = 'key', value_key: str = 'value'):
        self.variants = variants
        self.id_key = id_key
        self.value_key = value_key

    def get_buttons(self) -> list[list[types.InlineKeyboardButton]]:
        buttons = []
        for variant in self.variants:
            buttons.append(
                types.InlineKeyboardButton(
                    variant[self.value_key],
                    callback_data=f'{self.identifier}:select:{variant[self.id_key]}'
                )
            )
        return buttons

    def markup(self) -> types.InlineKeyboardMarkup:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(*self.get_buttons())
        return markup

    @classmethod
    def get_regexp(cls) -> str:
        return f'^{cls.identifier}:[\d\w\-\_]+:[\d\w\-\_]+$'


class CancelActionKeyboard:

    def __init__(self, language: str):
        self.language = language
    
    def markup(self) -> types.ReplyKeyboardMarkup:
        cancel_text = helpers.language.get_translation(self.language, 'cancel_button_label', 'Отмена')
        return types.ReplyKeyboardMarkup([
            [types.KeyboardButton(cancel_text)]
        ], resize_keyboard=True)

    @classmethod
    def is_cancel_message(cls, language, message_text) -> bool:
        cancel_text = helpers.language.get_translation(language, 'cancel_button_label', 'Отмена')
        return cancel_text == message_text


class DoneCancelKeyboard:

    def __init__(self, language: str):
        self.language = language
    
    def markup(self) -> types.ReplyKeyboardMarkup:
        done_text = helpers.language.get_translation(self.language, 'done_button_label', 'Готово')
        cancel_text = helpers.language.get_translation(self.language, 'cancel_button_label', 'Отмена')
        return types.ReplyKeyboardMarkup([
            [types.KeyboardButton(done_text)],
            [types.KeyboardButton(cancel_text)]
        ], resize_keyboard=True)

    @classmethod
    def is_done_message(cls, language, message_text) -> bool:
        done_text = helpers.language.get_translation(language, 'done_button_label', 'Готово')
        return message_text == done_text

    @classmethod
    def is_cancel_message(cls, language, message_text) -> bool:
        cancel_text = helpers.language.get_translation(language, 'cancel_button_label', 'Отмена')
        return cancel_text == message_text


class SelectObjectKeyboard:
    identifier: str = 'select_object_keyboard'

    def __init__(self, items: list[object], id_attr: str = 'pk', value_attr: str = 'name'):
        self.items = items
        self.id_attr = id_attr
        self.value_attr = value_attr

    def markup(self) -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup()
        for item in self.items:
            keyboard.row(
                types.InlineKeyboardButton(
                    getattr(item, self.value_attr, ''),
                    callback_data=f'{self.identifier}:select:{getattr(item, self.id_attr, "")}'
                )
            )
        return keyboard

    @classmethod
    def get_regexp(cls) -> str:
        return f'^{cls.identifier}:[\d\w\-\_]+:[\d\w\-\_]+$'
