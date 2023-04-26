from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from database.models import User


class UserMiddleware(BaseMiddleware):

    async def _prepare_user(self, user: types.User, data: dict):
        user, created = await User.get_by_telegram_id_or_create(
            user.id,
            user.username or '',
            user.first_name or '',
            user.last_name or '',
            user.language_code or ''
        )

        if not user.active:
            user.active = True

        if not user.is_business:
            user.is_business = True

        await user.save()

        data['user'] = user
        data['is_new_user'] = created

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self._prepare_user(message.from_user, data)

    async def on_pre_process_callback_query(self, query: types.InlineQuery, data: dict):
        await self._prepare_user(query.from_user, data)

"""
        if update.edited_message:
            current_user = update.edited_message.from_user
        if update.inline_query:
            current_user = update.inline_query.from_user
        if update.chosen_inline_result:
            current_user = update.chosen_inline_result.from_user
        if update.callback_query:
            current_user = update.callback_query.from_user
        if update.shipping_query:
            current_user = update.shipping_query.from_user
        if update.pre_checkout_query:
            current_user = update.pre_checkout_query.from_user
        if update.poll_answer:
            current_user = update.poll_answer.user
        if update.my_chat_member:
            current_user = update.my_chat_member.from_user
        if update.chat_member:
            current_user = update.chat_member.from_user
        if update.chat_join_request:
            current_user = update.chat_join_request.from_user
        if current_user != None:
            await self._prepare_user(current_user, data)
"""
