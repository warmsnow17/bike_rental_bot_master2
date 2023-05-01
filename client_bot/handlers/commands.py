import logging
import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from client_bot import dp, keyboards, states, constants, bot
from client_bot.constants import MANAGERS_UNAVAILABLE, CONTACT_MANAGER, SUBSCRIBE_TO_CHANNEL
from client_bot.keyboards import ChatWithManagerKeyboard
from client_bot.keyboards.main_menu import channel_keyboard
from database.models import User, Garage
import config


async def is_user_subscribed(message: types.Message):
    user_id = message.from_user.id
    try:
        member = await bot.get_chat_member(chat_id=os.getenv('CHANNEL_USERNAME_ID', ''), user_id=user_id)
        logging.info(f"Проверка подписки пользователя {user_id}: {member.status}")
        if member.status in ["member", "creator", "administrator"]:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Ошибка при проверке подписки пользователя {user_id}: {e}")
        return False


@dp.message_handler(state='*', commands=['start'])
async def start_command(message: types.Message, user: User, replies: dict[str, str], is_new_user: bool, state: FSMContext):

    user, created = await User.get_by_telegram_id_or_create(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.language_code
    )

    if not created and user.username != message.from_user.username:
        await user.update_username(message.from_user.username)

    if not await is_user_subscribed(message):
        return await prompt_user_to_subscribe(message, user)
    if state:
        await state.finish()
    me = await dp.bot.me
    reply_text = replies.get('welcome_message_reply', constants.WELCOME_MESSAGE_TEXT.get(user.language)).format(full_name=me.full_name)
    await message.answer(reply_text, reply_markup=None)

    # Select language
    reply_text = replies.get('initial_select_language', 'Выбери язык:').format(user=user)
    await states.SelectLanguageState.language.set()
    keyboard = keyboards.SelectLanguageKeyboard(config.CLIENT_BOT_LANGUAGES, id_key='code', value_key='native_name')
    await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state='*', commands=["restart_bot"])
async def restart_bot(message: types.Message, user: User, replies: dict[str, str], is_new_user: bool, state: FSMContext):
    user, created = await User.get_by_telegram_id_or_create(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.language_code
    )

    if not created and user.username != message.from_user.username:
        await user.update_username(message.from_user.username)

    if not await is_user_subscribed(message):
        return await prompt_user_to_subscribe(message, user)
    if state is not None:
        await state.finish()
    me = await dp.bot.me
    reply_text = replies.get('welcome_message_reply', constants.WELCOME_MESSAGE_TEXT.get(user.language)).format(full_name=me.full_name)
    await message.answer(reply_text, reply_markup=None)

    # Select language
    reply_text = replies.get('initial_select_language', 'Выбери язык:').format(user=user)
    await states.SelectLanguageState.language.set()
    keyboard = keyboards.SelectLanguageKeyboard(config.CLIENT_BOT_LANGUAGES, id_key='code', value_key='native_name')
    return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state='*', commands=["contact_manager"])
async def contact_manager(message: types.Message, user: User):
    if not await is_user_subscribed(message):
        return await prompt_user_to_subscribe(message, user)
    manager = await User.get_manager_for_user(user)
    if not manager:
        await message.answer(MANAGERS_UNAVAILABLE.get(user.language))
        return

    language = user.language
    chat_with_manager_keyboard = ChatWithManagerKeyboard(language, manager)
    await message.answer(CONTACT_MANAGER.get(user.language), reply_markup=chat_with_manager_keyboard.markup())


async def prompt_user_to_subscribe(message: types.Message, user: User):
    await message.reply(SUBSCRIBE_TO_CHANNEL.get(user.language), reply_markup=channel_keyboard())