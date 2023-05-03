from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_year():
    kb = InlineKeyboardMarkup(row_width=2)
    buttons = []
    for i in range(2018, 2024):
        button = InlineKeyboardButton(text=str(i), callback_data=i)
        buttons.insert(0, button)
    before_2018 = InlineKeyboardButton(text='До 2018', callback_data='До 2018')
    buttons.append(before_2018)
    kb.add(*buttons)
    return kb
