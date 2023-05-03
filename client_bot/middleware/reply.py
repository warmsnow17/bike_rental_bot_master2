from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from database.models import ReplyMessage
from client_bot import constants
import config


class ReplyMiddleware(BaseMiddleware):

    async def load_replies(self, data: dict):
        language = data.get('options', {}).get('default_language', config.DEFAULT_LANGUAGE)
        user = data.get('user', None)
        if user and user.language:
            language = user.language
        data['replies'] = constants.REPLIES[language]

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.load_replies(data)

    async def on_pre_process_callback_query(self, query: types.InlineQuery, data: dict):
        await self.load_replies(data)
