from aiogram import types
from aiogram.dispatcher import FSMContext
from client_bot import dp, keyboards, states, constants
from database.models import User, Garage
import config


@dp.message_handler(state='*', commands=['start'])
async def start(message: types.Message, user: User, replies: dict[str, str], is_new_user: bool, state: FSMContext):
    if state:
        await state.finish()
    me = await dp.bot.me

    # Select language
    reply_text = replies.get('initial_select_language', 'Выбери язык:').format(user=user)
    await states.SelectLanguageState.language.set()
    keyboard = keyboards.SelectLanguageKeyboard(config.CLIENT_BOT_LANGUAGES, id_key='code', value_key='native_name')
    await message.answer(reply_text, reply_markup=keyboard.markup())
    reply_text = replies.get('welcome_message_reply', constants.WELCOME_MESSAGE_TEXT.get(user.language)).format(full_name=me.full_name)
    await message.answer(reply_text, reply_markup=None)
