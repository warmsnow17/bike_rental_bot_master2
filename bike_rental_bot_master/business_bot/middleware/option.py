from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from database.models import Option


class OptionMiddleware(BaseMiddleware):

    async def load_options(self, data: dict):
        options = await Option.all()
        data['options'] = {}
        for option in options:
            data['options'][option.key] = option.value

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.load_options(data)

    async def on_pre_process_callback_query(self, query: types.InlineQuery, data: dict):
        await self.load_options(data)
