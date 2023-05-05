from aiogram import types, filters, Dispatcher
from aiogram.dispatcher import FSMContext
from business_bot import dp, keyboards, states, constants
from database.models import User
from loguru import logger


@dp.callback_query_handler(filters.Regexp(keyboards.SelectLanguageKeyboard.get_regexp()), state=states.SelectLanguageState.language)
async def language_selected(query: types.CallbackQuery, user: User, state: FSMContext):
    _, _, selected_language = query.data.split(':', maxsplit=2)
    user.language = selected_language
    logger.warning(selected_language)
    await user.save()
    if user.language == 'id':
        text = constants.AGREEMENT_id

    if user.language == 'en':
        text = constants.AGREEMENT_en

    if user.language == 'ru':
        text = constants.AGREEMENT_ru
    await query.message.answer(text,
                               reply_markup=keyboards.language.accept_kb())
    await state.set_state(states.language.SelectLanguageState.agreement)


@dp.callback_query_handler(text='accept', state=states.language.SelectLanguageState.agreement)
async def agreement_accepted(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    current_state = await state.get_data()
    await state.finish()
    await query.message.delete()
    if current_state.get('initial_setup'):
        bot = await dp.bot.me
        reply_text = replies.get('welcome_message', constants.WELCOME_MESSAGE.get(user.language)).format(full_name=bot.full_name)
        await query.message.answer(reply_text, reply_markup=None)
        reply_text = replies.get('enter_garage_location', 'Где находится гараж?(Отправьте координаты)').format(user=user)
        await states.SetupGarageState.location.set()
        return await query.message.answer(reply_text, reply_markup=types.ReplyKeyboardRemove())
    await states.MainMenuState.not_selected.set()
    if current_state.get('welcome_message'):
        bot = await dp.bot.me
        reply_text = replies.get('welcome_message', constants.WELCOME_MESSAGE.get(user.language)).format(full_name=bot.full_name)
        await query.message.answer(reply_text, reply_markup=None)
    reply_text = replies.get('initial_main_menu_reply', 'Добро пожаловать в виртуальный офис! Выбери нужное действие из списка').format(user=user)
    keyboard = keyboards.MainMenuKeyboard(language=user.language)
    await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.SelectLanguageState.language)
async def language_not_selected(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    reply_text = replies.get('select_language_error', 'Выбери язык из списка').format(user=user)
    await message.reply(reply_text)
