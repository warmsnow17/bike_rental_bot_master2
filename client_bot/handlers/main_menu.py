from aiogram import types
from aiogram.dispatcher import FSMContext
from client_bot import dp, states, keyboards, constants
from client_bot.keyboards import other
from database.models import User, BikeModel
import config
from loguru import logger


@dp.message_handler(
    state=[states.MainMenuState.not_selected, states.RentRequestState.prepare, states.SelectLanguageState.language]
)
async def menu_button_select(message: types.Message, user: User, replies: dict[str, str], state: FSMContext, options: dict[str, str]):
    if state:
        await state.finish()
        await states.MainMenuState.not_selected.set()
    idr_exchange_rate = float(options.get('idr_per_usd_exchange_rate', 15100))
    button_id = keyboards.MainMenuKeyboard.get_button_id_by_text(user.language, message.text)
    if button_id == 'rent_a_bike_button_label':
        await state.set_state(states.RentRequestState.model)
        reply_text = replies.get('rent_a_bike_init_reply', 'Заполни заявку на аренду').format(user=user)
        keyboard = keyboards.CancelActionKeyboard(language=user.language)
        await message.answer(reply_text, reply_markup=keyboard.markup())
        reply_text = replies.get('rent_a_bike_reply', 'Какую модель хочешь?').format(user=user)
        models = await BikeModel.all()
        logger.warning(models)
        keyboard = keyboards.SelectBikeModelKeyboard(models, user.language, idr_exchange_rate)
        return await message.answer(reply_text, reply_markup=await keyboard.markup())
    elif button_id == 'model_help_button_label':
        await states.RentRequestState.help.set()
        reply_text = replies.get('rent_a_bike_init_reply', constants.HELP_MESSAGE_TEXT).format(user=user)
        # models = await BikeModel.all()
        keyboard = other.bikes()
        message = await message.answer(reply_text, reply_markup=keyboard)
        # return await message.answer(reply_text, reply_markup=keyboard.markup())
    elif button_id == 'select_language_button_label':
        reply_text = replies.get('select_language', 'Выбери язык:').format(user=user)
        await states.SelectLanguageState.language.set()
        keyboard = keyboards.SelectLanguageKeyboard(config.CLIENT_BOT_LANGUAGES, id_key='code', value_key='native_name')
        return await message.answer(reply_text, reply_markup=keyboard.markup())
    else:
        reply_text = replies.get('select_main_menu_action', 'Выберите действие из списка').format(user=user)
        keyboard = keyboards.MainMenuKeyboard(user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())
