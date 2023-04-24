from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from client_bot import dp, keyboards, states
from database.models import User


@dp.callback_query_handler(filters.Regexp(keyboards.SelectLanguageKeyboard.get_regexp()), state=states.SelectLanguageState.language)
async def language_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, selected_language = query.data.split(':', maxsplit=2)
    user.language = selected_language
    await user.save()
    await state.finish()
    await query.message.delete()
    await states.MainMenuState.not_selected.set()
    reply_text = replies.get('main_menu_reply', 'Ты оказался в главном меню').format(user=user)
    keyboard = keyboards.MainMenuKeyboard(language=user.language)
    await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.SelectLanguageState.language)
async def language_not_selected(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    reply_text = replies.get('select_language_error', 'Выбери язык из списка').format(user=user)
    await message.reply(reply_text)
