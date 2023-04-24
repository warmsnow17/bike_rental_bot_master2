from aiogram import types, filters, Dispatcher
from aiogram.dispatcher import FSMContext
from business_bot import dp, keyboards, states, constants
from database.models import User


@dp.callback_query_handler(filters.Regexp(keyboards.SelectLanguageKeyboard.get_regexp()), state=states.SelectLanguageState.language)
async def language_selected(query: types.CallbackQuery, user: User, state: FSMContext):
    _, _, selected_language = query.data.split(':', maxsplit=2)
    user.language = selected_language
    await user.save()
    await query.message.answer(constants.AGREEMENT,
                               reply_markup=keyboards.language.accept_kb())
    await state.set_state(states.language.SelectLanguageState.agreement)


@dp.callback_query_handler(text='accept', state=states.language.SelectLanguageState.agreement)
async def agreement_accepted(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    current_state = await state.get_data()
    await state.finish()
    await query.message.delete()
    if current_state.get('initial_setup'):
        reply_text = replies.get('enter_garage_owner_name', 'Для начала работы заполни информацию о себе. Как тебя зовут?').format(user=user)
        await states.SetupGarageState.owner_name.set()
        return await query.message.answer(reply_text, reply_markup=types.ReplyKeyboardRemove())
    await states.MainMenuState.not_selected.set()
    reply_text = replies.get('main_menu_reply', 'Добро пожаловать в виртуальный офис! Выбери нужное действие из списка').format(user=user)
    keyboard = keyboards.MainMenuKeyboard(language=user.language)
    await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.SelectLanguageState.language)
async def language_not_selected(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    reply_text = replies.get('select_language_error', 'Выбери язык из списка').format(user=user)
    await message.reply(reply_text)
