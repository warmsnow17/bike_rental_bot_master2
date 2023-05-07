from .base import SelectInlineKeyboard
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class SelectLanguageKeyboard(SelectInlineKeyboard):
    identifier = 'select_language_keyboard'


def accept_kb():
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    button = InlineKeyboardButton('Accept', callback_data='accept')
    kb.row(button)
    return kb
