from aiogram import types
from aiogram.dispatcher import FSMContext
from business_bot import dp, keyboards, states, constants
from database.models import User, Garage
import config


@dp.message_handler(state='*', commands=['start'])
async def start(message: types.Message, user: User, replies: dict[str, str], is_new_user: bool, state: FSMContext):
    if state:
        await state.finish()

    bot = await dp.bot.me
    reply_text = replies.get('welcome_message', constants.WELCOME_MESSAGE.get(user.language)).format(full_name=bot.full_name)
    await message.answer(reply_text, reply_markup=None)

    # Select language
    reply_text = replies.get('select_language', 'Выбери язык:').format(user=user)
    await states.SelectLanguageState.language.set()
    state = dp.current_state()
    await state.update_data(initial_setup=not await user.has_garages())
    keyboard = keyboards.SelectLanguageKeyboard(config.BUSINESS_BOT_LANGUAGES, id_key='code', value_key='native_name')
    return await message.answer(reply_text, reply_markup=keyboard.markup())

