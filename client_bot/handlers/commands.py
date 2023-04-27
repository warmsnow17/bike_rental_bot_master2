from aiogram import types
from aiogram.dispatcher import FSMContext
from client_bot import dp, keyboards, states, constants
from client_bot.keyboards import ChatWithManagerKeyboard
from database.models import User, Garage
import config


@dp.message_handler(state='*', commands=['start'])
async def start(message: types.Message, user: User, replies: dict[str, str], is_new_user: bool, state: FSMContext):
    if state:
        await state.finish()
    me = await dp.bot.me
    reply_text = replies.get('welcome_message_reply', constants.WELCOME_MESSAGE_TEXT.get(user.language)).format(full_name=me.full_name)
    await message.answer(reply_text, reply_markup=None)

    # Select language
    reply_text = replies.get('initial_select_language', 'Выбери язык:').format(user=user)
    await states.SelectLanguageState.language.set()
    keyboard = keyboards.SelectLanguageKeyboard(config.CLIENT_BOT_LANGUAGES, id_key='code', value_key='native_name')
    return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state='*', commands=["restart_bot"])
async def restart_bot(message: types.Message, user: User, replies: dict[str, str], is_new_user: bool, state: FSMContext):
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
    manager = await User.get_manager_for_user(user)
    if not manager:
        await message.answer("Извините, в данный момент менеджеры недоступны.")
        return

    language = user.language
    chat_with_manager_keyboard = ChatWithManagerKeyboard(language, manager)
    await message.answer("Вы можете связаться с менеджером, нажав на кнопку ниже:", reply_markup=chat_with_manager_keyboard.markup())
