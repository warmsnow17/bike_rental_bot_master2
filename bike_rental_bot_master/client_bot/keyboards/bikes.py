from datetime import datetime
from aiogram import types
from client_bot import helpers
from .base import SelectObjectKeyboard


class SelectBikeModelKeyboard(SelectObjectKeyboard):
    identifier: str = 'select_bike_model'

    def __init__(self, items: list[object], language: str, exchange_rate: float, id_attr: str = 'pk', value_attr: str = 'name'):
        super().__init__(items, id_attr, value_attr)
        self.language = language
        self.exchange_rate = exchange_rate

    async def markup(self) -> types.InlineKeyboardMarkup:
        keyboard = types.InlineKeyboardMarkup()
        for item in self.items:
            bikes_available = await item.has_available_bikes(datetime.now())
            if not bikes_available:
                continue
            price = round(float(await item.get_lowes_price()) / self.exchange_rate, 2)
            if price > 0:
                fr = helpers.language.get_translation(self.language, 'from_label', 'from_label')
                label = f'{item.name} - {fr} {price}$'
            else:
                label = f'{item.name}'
            keyboard.row(
                types.InlineKeyboardButton(
                    label,
                    callback_data=f'{self.identifier}:select:{getattr(item, self.id_attr, "")}'
                )
            )
        return keyboard
