from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from client_bot import constants
import os

callback_bike = CallbackData('bike', 'name', 'photo')


def bikes():
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for bike in constants.BIKES:
        for filename in os.listdir('client_bot/photos'):
            if f'{bike.lower()}.jpeg' == filename:
                path = filename
        button = InlineKeyboardButton(text=bike,
                                      callback_data=callback_bike.new(name=bike,
                                                                      photo=path))
        buttons.append(button)
    kb.add(*buttons)
    return kb


def choose_or_back():
    kb = InlineKeyboardMarkup(resize_keyboard=True)
    b1 = InlineKeyboardButton(text='Выбрать', callback_data='choose_help')
    b2 = InlineKeyboardButton(text='Назад', callback_data='back_help')
    kb.row(b1, b2)
    return kb