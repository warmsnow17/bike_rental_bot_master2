from aiogram import types
from aiogram.dispatcher import FSMContext
from business_bot import dp, keyboards, states, constants
from database.models import User, Garage
import config


@dp.message_handler(state='*', commands=['start'])
async def start(message: types.Message, user: User, replies: dict[str, str], is_new_user: bool, state: FSMContext):
    if state:
        await state.finish()

    # Select language
    reply_text = replies.get('select_language', 'Выбери язык:').format(user=user)
    await states.SelectLanguageState.language.set()
    state = dp.current_state()
    await state.update_data(initial_setup=not await user.has_garages(), welcome_message=True)
    keyboard = keyboards.SelectLanguageKeyboard(config.BUSINESS_BOT_LANGUAGES, id_key='code', value_key='native_name')
    return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state='*', commands=['update_garage'])
async def update_garage(message: types.Message, user: User, replies: dict[str, str], is_new_user: bool, state: FSMContext):
    if state:
        await state.finish()
    reply_text = replies.get('enter_garage_location', 'Где находится гараж?(Отправьте координаты)').format(user=user)
    await states.SetupGarageState.location.set()
    state = dp.current_state()
    await state.update_data(update=True)
    return await message.answer(reply_text, reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state='*', commands=['office'])
async def office(message: types.Message, user: User, replies: dict[str, str], is_new_user: bool, state: FSMContext):
    if state:
        await state.finish()
    reply_text = replies.get(
        'back_main_menu_reply',
        'Действие отменено.'
    ).format(user=user)
    await states.MainMenuState.not_selected.set()
    keyboard = keyboards.MainMenuKeyboard(language=user.language)
    await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state='*', commands=['help'])
async def start(message: types.Message, user: User, replies: dict[str, str], is_new_user: bool, state: FSMContext):
    if state:
        await state.finish()

    await states.BotMenuState.help.set()
    reply_text = replies.get(
        'back_main_menu_reply',
        'Действие отменено.'
    ).format(user=user)
    keyboard = keyboards.MainMenuKeyboard(language=user.language)
    await message.answer(reply_text, reply_markup=keyboard.markup())

    reply_text = replies.get('help_message', 'Для связи с менеджером нажмите на кнопку').format()
    manager = await User.get_random_manager()
    keyboard = keyboards.ManagerKeyboard(user.language, manager)
    await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state='*', commands=['language'])
async def start(message: types.Message, user: User, replies: dict[str, str], is_new_user: bool, state: FSMContext):
    if state:
        await state.finish()
    await states.BotMenuState.language.set()
    reply_text = replies.get('select_language', 'Выбери язык:').format(user=user)
    await states.SelectLanguageState.language.set()
    state = dp.current_state()
    await state.update_data(initial_setup=not await user.has_garages())
    keyboard = keyboards.SelectLanguageKeyboard(config.BUSINESS_BOT_LANGUAGES, id_key='code', value_key='native_name')
    return await message.answer(reply_text, reply_markup=keyboard.markup())