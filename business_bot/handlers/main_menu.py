from aiogram import types
from aiogram.dispatcher import FSMContext
from business_bot import dp, states, keyboards, helpers
from database.models import User, BikeModel, BikeBooking



@dp.message_handler(
    state=[states.MainMenuState.not_selected, states.GarageState.bikes_list, states.GarageState.bike_details, states.CalendarState.calendar]
)
async def menu_button_select(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if state:
        await state.finish()
        await states.MainMenuState.not_selected.set()
    button_id = keyboards.MainMenuKeyboard.get_button_id_by_text(user.language, message.text)
    if button_id == 'add_bike_button_label':
        await states.BikeState.model.set()
        reply_text = replies.get('bike_state_initial', 'Чтобы добавить байк, ответь на вопросы:').format(user=user)
        keyboard = keyboards.CancelActionKeyboard(language=user.language)
        await message.answer(reply_text, reply_markup=keyboard.markup())
        reply_text = replies.get('select_bike_model', 'Выбери модель байка из списка:').format(user=user)
        bike_models = await BikeModel.all()
        keyboard = keyboards.SelectBikeModelKeyboard(bike_models)
        return await message.answer(reply_text, reply_markup=keyboard.markup())
    elif button_id == 'my_garage_button_label':
        await states.GarageState.bikes_list.set()
        reply_text = replies.get('my_bikes_reply', 'Здесь ты можешь посмотреть доступные байки и байки в аренде').format(user=user)
        keyboard = keyboards.GarageBikesKeyboard(user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())
    elif button_id == 'rental_calendar_button_label':
        bookings = await BikeBooking.filter(bike__user=user).order_by('id').select_related('bike', 'bike__model', 'offer', 'offer__request')
        if len(bookings) == 0:
            reply_text = replies.get('no_complete_offers_reply', 'Нет заказов').format(user=user)
            return await message.answer(reply_text)
        report = helpers.report.get_report(bookings)
        return await message.answer_document(
            types.InputFile(report, filename='report.xlsx') 
        )
    else:
        reply_text = replies.get('select_main_menu_action', 'Выберите действие из списка').format(user=user)
        keyboard = keyboards.MainMenuKeyboard(user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())
