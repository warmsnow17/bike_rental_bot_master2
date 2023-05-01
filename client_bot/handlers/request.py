import asyncio
from datetime import datetime, timedelta
from aiogram import types, filters, exceptions
from aiogram.dispatcher import FSMContext
from client_bot import dp, keyboards, states, helpers, constants
from business_bot import dp as business_bot_dp
from database.models import User, BikeModel, RentalRequest, Bike, BikeOffer, BikeBooking


@dp.callback_query_handler(filters.Regexp(keyboards.SelectBikeModelKeyboard.get_regexp()), state=states.RentRequestState.prepare)
async def prepare_bike_model_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, model_id = query.data.split(':', maxsplit=2)
    model = await BikeModel.get_or_none(pk=int(model_id))
    await state.update_data(model=model_id, model_name=model.name if model else '')
    await query.message.edit_reply_markup(None)
    new_message_text = replies.get('prepare_bike_model_selected', 'Выбрана модель: {model.name}').format(model=model)
    await query.message.answer(new_message_text, reply_markup=keyboards.CancelActionKeyboard(user.language).markup())

    reply_text = replies.get('request_additional_params_reply', 'Хочешь указать дополнительные параметры байка?').format(user=user)
    await states.RentRequestState.additional_params.set()
    keyboard = keyboards.AdditionalParamsKeyboard(user.language)
    return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.SelectBikeModelKeyboard.get_regexp()), state=states.RentRequestState.model)
async def bike_model_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, model_id = query.data.split(':', maxsplit=2)
    model = await BikeModel.get_or_none(pk=int(model_id))
    await state.update_data(model=model_id, model_name=model.name if model else '')
    new_message_text = replies.get('bike_model_selected', 'Выбрана модель: {model.name}').format(model=model)
    await query.message.edit_text(new_message_text, reply_markup=None)

    reply_text = replies.get('request_additional_params_reply', 'Хочешь указать дополнительные параметры байка?').format(user=user)
    await states.RentRequestState.additional_params.set()
    keyboard = keyboards.AdditionalParamsKeyboard(user.language)
    return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.RentRequestState.model)
async def model_text(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        await state.finish()
        reply_text = replies.get(
            'back_client_menu_reply',
            'Запрос отменен. Ты вернулся в главное меню.'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.AdditionalParamsKeyboard.get_regexp()), state=states.RentRequestState.additional_params)
async def bike_addition_params_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, answer = query.data.split(':', maxsplit=2)
    if answer == 'yes':
        await state.update_data(additional_params=True)
        await query.message.delete()
        reply_text = replies.get('request_year_select', 'Хочешь ли ты ограничить год выпуска?').format(user=user)
        await states.RentRequestState.year.set()
        keyboard = keyboards.RequestYearKeyboard(user.language)
        return await query.message.answer(reply_text, reply_markup=keyboard.markup())
    if answer == 'no':
        await state.update_data(additional_params=False)
        await query.message.delete()
        reply_text = replies.get('request_helmets_select', 'Сколько шлемов тебе понадобится?').format(user=user)
        await states.RentRequestState.helmets.set()
        keyboard = keyboards.RequestHelmetsKeyboard(user.language)
        return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.RentRequestState.additional_params)
async def additional_params_text(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        await state.finish()
        reply_text = replies.get(
            'back_client_menu_reply',
            'Запрос отменен. Ты вернулся в главное меню.'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.RequestYearKeyboard.get_regexp()), state=states.RentRequestState.year)
async def bike_year_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, year = query.data.split(':', maxsplit=2)
    await state.update_data(year=year)
    keyboard = keyboards.RequestYearKeyboard(user.language)
    reply_text = replies.get('requested_year_limit_label', 'Ограничение по году: {year_limit}').format(year_limit=keyboard.get_variant_label(year))
    await query.message.edit_text(reply_text, reply_markup=None)
    reply_text = replies.get('request_color_select', 'Есть ли у тебя предпочтения по цвету?').format(user=user)
    await states.RentRequestState.color.set()
    keyboard = keyboards.RequestColorSelectionKeyboard(user.language)
    return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.RentRequestState.year)
async def year_text(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        await state.finish()
        reply_text = replies.get(
            'back_client_menu_reply',
            'Запрос отменен. Ты вернулся в главное меню.'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())


"""@dp.callback_query_handler(filters.Regexp(keyboards.RequestMileageKeyboard.get_regexp()), state=states.RentRequestState.mileage)
async def bike_mileage_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, mileage = query.data.split(':', maxsplit=2)
    await state.update_data(mileage=mileage)
    await query.message.delete()
    reply_text = replies.get('request_color_select', 'Вебри желаемый цвет байка').format(user=user)
    await states.RentRequestState.color.set()
    keyboard = keyboards.RequestColorSelectionKeyboard(user.language)
    return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.RentRequestState.mileage)
async def mileage_text(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        await state.finish()
        reply_text = replies.get(
            'back_client_menu_reply',
            'Запрос отменен. Ты вернулся в главное меню.'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())"""


@dp.callback_query_handler(filters.Regexp(keyboards.RequestColorSelectionKeyboard.get_regexp()), state=states.RentRequestState.color)
async def bike_color_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, color = query.data.split(':', maxsplit=2)
    await state.update_data(color=color)
    keyboard = keyboards.RequestColorSelectionKeyboard(user.language)
    reply_text = replies.get('requested_color_limit_label', 'Предпочитаемый цвет: {color}').format(color=keyboard.get_variant_label(color))
    await query.message.edit_text(reply_text, reply_markup=None)
    reply_text = replies.get('request_abs_select', 'Нужен ли ABS?').format(user=user)
    await states.RentRequestState.abs.set()
    keyboard = keyboards.RequestABSSelectionKeyboard(user.language)
    return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.RentRequestState.color)
async def color_text(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        await state.finish()
        reply_text = replies.get(
            'back_client_menu_reply',
            'Запрос отменен. Ты вернулся в главное меню.'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.RequestABSSelectionKeyboard.get_regexp()), state=states.RentRequestState.abs)
async def bike_abs_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, abs = query.data.split(':', maxsplit=2)
    await state.update_data(abs=abs)
    if abs == 'yes':
        reply_text = replies.get('requested_abs_required_label', 'Нужен ABS')
    elif abs == 'no':
        reply_text = replies.get('requested_abs_not_required_label', 'ABS не нужен')
    else:
        reply_text = replies.get('requested_abs_any_label', 'Наличие ABS неважно')
    await query.message.edit_text(reply_text, reply_markup=None)
    reply_text = replies.get('request_keyless_select', 'Нужен ли Keyless доступ?').format(user=user)
    await states.RentRequestState.keyless.set()
    keyboard = keyboards.RequestKeylessSelectionKeyboard(user.language)
    return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.RentRequestState.abs)
async def abs_text(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        await state.finish()
        reply_text = replies.get(
            'back_client_menu_reply',
            'Запрос отменен. Ты вернулся в главное меню.'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.RequestKeylessSelectionKeyboard.get_regexp()), state=states.RentRequestState.keyless)
async def bike_keyless_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, keyless = query.data.split(':', maxsplit=2)
    await state.update_data(keyless=keyless)
    if keyless == 'yes':
        reply_text = replies.get('requested_keyless_required_label', 'Нужен Keyless доступ')
    elif keyless == 'no':
        reply_text = replies.get('requested_keyless_not_required_label', 'Keyless доступ не нужен')
    else:
        reply_text = replies.get('requested_keyless_any_label', 'Наличие Keyless доступа неважно')
    await query.message.edit_text(reply_text, reply_markup=None)
    reply_text = replies.get('request_helmets_select', 'Сколько шлемов тебе понадобится?').format(user=user)
    await states.RentRequestState.helmets.set()
    keyboard = keyboards.RequestHelmetsKeyboard(user.language)
    return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.RentRequestState.keyless)
async def keyless_text(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        await state.finish()
        reply_text = replies.get(
            'back_client_menu_reply',
            'Запрос отменен. Ты вернулся в главное меню.'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.RentRequestState.helmets)
async def helmets_message(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        await state.finish()
        reply_text = replies.get(
            'back_client_menu_reply',
            'Запрос отменен. Ты вернулся в главное меню.'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.RequestHelmetsKeyboard.get_regexp()), state=states.RentRequestState.helmets)
async def helmets_amount_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, action, helmets = query.data.split(':', maxsplit=2)
    if helmets == 'one':
        await state.update_data(helmets=1)
        reply_text = replies.get('requested_one_helmet_required_label', 'Один шлем')
    elif helmets == 'two':
        await state.update_data(helmets=2)
        reply_text = replies.get('requested_two_helmets_required_label', 'Два шлема')
    else:
        await state.update_data(helmets=0)
        reply_text = replies.get('requested_no_helmets_label', 'Шлемы не нужны')
    await query.message.edit_text(reply_text, reply_markup=None)
    await states.RentRequestState.rent_start_date.set()
    keyboard = keyboards.RequestRentStartDateKeyboard(user.language)
    reply_text = replies.get('request_rent_start_select', 'Укажи когда ты хочешь начать аренду?').format(user=user)
    return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(state=states.RentRequestState.rent_start_date)
async def bike_rent_start_date_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext, options: dict[str, str]):
    _, action, params = query.data.split(':', maxsplit=2)
    if action == 'sw':
        year, month, day = params.split(':')
        keyboard = keyboards.RequestRentStartDateKeyboard(user.language, int(month), int(year))
        return await query.message.edit_reply_markup(keyboard.markup())
    if action == 'sl':
        year, month, day = params.split(':')
        start_date = datetime(int(year), int(month), int(day), 0, 0, 0, 0)
        await state.update_data(rent_start_date=str(start_date.date()))
        reply_text = replies.get('rent_start_date_selected_reply', 'Дата начала аренды: {rent_start_date}').format(rent_start_date=start_date.date())
        await query.message.edit_text(reply_text, reply_markup=None)
        await states.RentRequestState.rent_end_date.set()
        keyboard = keyboards.RequestRentStartDateKeyboard(user.language)
        reply_text = replies.get('request_rent_type_select', 'Укажи когда ты планируешь вернуть байк?').format(user=user)
        return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(state=states.RentRequestState.rent_end_date)
async def bike_rent_end_date_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext, options: dict[str, str]):
    _, action, params = query.data.split(':', maxsplit=2)
    if action == 'sw':
        year, month, day = params.split(':')
        keyboard = keyboards.RequestRentStartDateKeyboard(user.language, int(month), int(year))
        return await query.message.edit_reply_markup(keyboard.markup())
    if action == 'sl':
        data = await state.get_data()
        year, month, day = params.split(':')
        end_date = datetime(int(year), int(month), int(day), 0, 0, 0, 0)
        await state.update_data(rent_end_date=str(end_date.date()))
        reply_text = replies.get('rent_end_date_selected_reply', 'Дата конца аренды: {rent_end_date}').format(rent_end_date=end_date.date())
        await query.message.edit_text(reply_text, reply_markup=None)
        await states.RentRequestState.location.set()
        reply_text = replies.get('rent_delivery_location_reply', 'Пришли, пожалуйста, локацию, куда нужно доставить байк')
        await query.message.answer(reply_text, reply_markup=None)


@dp.message_handler(state=states.RentRequestState.rent_start_date)
async def rent_start_date_text(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        await state.finish()
        reply_text = replies.get(
            'back_client_menu_reply',
            'Запрос отменен. Ты вернулся в главное меню.'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.RentRequestState.rent_end_date)
async def rent_end_date_text(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        await state.finish()
        reply_text = replies.get(
            'back_client_menu_reply',
            'Запрос отменен. Ты вернулся в главное меню.'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.RentRequestState.location)
async def location_message(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        await state.finish()
        reply_text = replies.get(
            'back_client_menu_reply',
            'Запрос отменен. Ты вернулся в главное меню.'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())

    else:
        await message.reply("Пожалуйста, используйте встроенную функцию Telegram для отправки геолокации.")
        return



@dp.message_handler(state=states.RentRequestState.location, content_types=[types.ContentType.LOCATION, types.ContentType.VENUE])
async def rent_request_delivery_location(message: types.Message, user: User, replies: dict[str, str], state: FSMContext, options: dict[str, str]):

    if message.content_type == types.ContentType.LOCATION:
        lat = message.location.latitude
        lon = message.location.longitude
    else: # message.content_type == types.ContentType.VENUE
        lat = message.venue.location.latitude
        lon = message.venue.location.longitude

    await state.update_data(lat=lat, lon=lon)
    reply_text = replies.get('rent_delivery_location_selected_reply', 'Координаты получены!')
    await states.RentRequestState.request_confirmation.set()
    data = await state.get_data()
    if data.get('additional_params'):
        reply_text = replies.get('rent_delivery_location_selected_reply', constants.ORDER_CONFIRMATION).format(
            model_obj=await BikeModel.get(pk=data['model']),
            color_label=helpers.language.get_translation(user.language, '{}_color_label'.format(data.get('color')), data.get('color')),
            keyless_label=helpers.language.get_translation(user.language, 'request_{}_answer_label'.format(data.get('keyless')), data.get('keyless')),
            abs_label=helpers.language.get_translation(user.language, 'request_{}_answer_label'.format(data.get('abs')), data.get('abs')),
            helmets_label=helpers.language.get_translation(user.language, '{}_helmets_label'.format(data.get('helmets', 'no')), data.get('helmets', 'no')),
            **data
        )
    else:
        reply_text = replies.get('rent_delivery_location_selected_reply', constants.SIMPLE_ORDER_CONFIRMATION).format(
            model_obj=await BikeModel.get(pk=data['model']),
            color_label=helpers.language.get_translation(user.language, '{}_color_label'.format(data.get('color')), data.get('color')),
            keyless_label=helpers.language.get_translation(user.language, 'request_{}_answer_label'.format(data.get('keyless')), data.get('keyless')),
            abs_label=helpers.language.get_translation(user.language, 'request_{}_answer_label'.format(data.get('abs')), data.get('abs')),
            helmets_label=helpers.language.get_translation(user.language, '{}_helmets_label'.format(data.get('helmets', 'no')), data.get('helmets', 'no')),
            rent_type_label=helpers.language.get_translation(user.language, '{}_rent_label'.format(data.get('rent_type')), data.get('rent_type')),
            rent_type_amount_label=helpers.language.get_translation(user.language, '{}_rent_type_amount_label'.format(data.get('rent_type')), data.get('rent_type')),
            **data
        )
    await message.answer(reply_text, reply_markup=keyboards.ConfirmationKeyboard(language=user.language).markup())


@dp.callback_query_handler(state=states.RentRequestState.request_confirmation)
async def rent_request_answer_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext, options: dict[str, str]):
    data = await state.get_data()
    start_date = datetime.fromisoformat(data.get('rent_start_date'))
    end_date = datetime.fromisoformat(data.get('rent_end_date'))
    rent_amount = (end_date - start_date).days
    if rent_amount < 7:
        rent_type = 'daily'
    elif rent_amount < 14:
        rent_type = 'weekly'
    elif rent_amount < 30:
        rent_type = 'biweekly'
    else:
        rent_type = 'monthly'
    manager = await User.get_random_manager()
    rent_request = await RentalRequest.create(
        user=user,
        manager=manager,
        model=await BikeModel.get_or_none(pk=data.get('model')),
        additional_params=data.get('additional_params'),
        year_from=int(data.get('year', 0)) if data.get('year', 0) != 'any' else 0,
        mileage_to=int(data.get('mileage', 0)) if data.get('mileage', 0) != 'any' else 0,
        helmets=data.get('helmets', 0),
        lat=data.get('lat'),
        lon=data.get('lon'),
        color=data.get('color', ''),
        abs=data.get('abs', 'any'),
        keyless=data.get('keyless', 'any'),
        rent_type=rent_type,
        rent_amount=rent_amount,
        rent_start_date=data.get('rent_start_date'),
        rent_end_date=data.get('rent_end_date')
    )
    bikes = await Bike.get_for_request(rent_request)
    await query.message.edit_reply_markup(None)
    if len(bikes) > 0:
        await states.ActiveRequestState.request_id.set()
        state = dp.current_state()
        await state.update_data(request_id=rent_request.pk)
        reply_text = replies.get(
            'request_complete_ask_reply',
            """Номер заявки: {request.pk}
Сейчас я опрашиваю сервисы аренды. Поиск продлится не более {request_lifetime} минут.
По мере подверждения предложения начнут появляться в чате""".format(
    request_lifetime=options.get('bike_request_lifetime', 5),
    request=rent_request
)
        ).format(user=user)
        keyboard = keyboards.RequestCreatedKeyboard(user.language)
        await query.message.answer(reply_text, reply_markup=keyboard.markup())

        for bike in bikes:
            try:
                await rent_request.refresh_from_db()
            except:
                break
            if rent_request.selected_offer_id is not None:
                break
            if rent_request.rent_type == 'daily':
                price = bike.price
                price_with_fee = float(bike.price) + (float(bike.price) * (int(options.get('fee_percent', 10)) / 100.0))
            if rent_request.rent_type == 'weekly':
                price = bike.weekly_price / 7
                price_with_fee = float(price) + (float(price) * (int(options.get('fee_percent', 10)) / 100.0))
            if rent_request.rent_type == 'biweekly':
                price = bike.biweekly_price / 14
                price_with_fee = float(price) + (float(price) * (int(options.get('fee_percent', 10)) / 100.0))
            if rent_request.rent_type == 'monthly':
                price = bike.monthly_price / 30
                price_with_fee = float(price) + (float(price) * (int(options.get('fee_percent', 10)) / 100.0))
            offer = await BikeOffer.create(
                bike=bike,
                client=user,
                request=rent_request,
                price=price,
                price_with_fee=price_with_fee,
                total_sum=price * rent_request.rent_amount,
                total_sum_with_fee=price_with_fee * rent_request.rent_amount
            )
            business_replies = constants.REPLIES.get(bike.user.language)
            message_text = business_replies.get(
                'new_rental_request',
                'Привет! Интересует {bike.model.name} на {rent_amount} дней с {start_date} \n\n Он свободен сейчас?'
            ).format(bike=bike, rent_amount=rent_amount, start_date=start_date.strftime("%d.%m.%Y"))
            keyboard = keyboards.NewBikeRentRequestKeyboard(bike.user.language, offer.pk)
            message = await helpers.message.send_message(
                business_bot_dp.bot,
                bike.user.telegram_id,
                message_text,
                keyboard.markup()
            )
            if not message:
                await offer.delete()
            else:
                offer.business_message_id = message.message_id
                await offer.save()
    else:
        await states.MainMenuState.not_selected.set()
        reply_text = replies.get(
            'request_complete_nothing_found_reply',
            'Нет подходящих байков. Попробуй изменить параметры поиска'
        ).format(user=user)
        keyboard = keyboards.MainMenuKeyboard(user.language)
        return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.RentRequestState.request_confirmation)
async def rent_confirmation_message(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        await state.finish()
        reply_text = replies.get(
            'back_client_menu_reply',
            'Запрос отменен. Ты вернулся в главное меню.'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.AcceptOfferKeyboard.get_regexp()), state='*')
async def accept_offer(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, action, offer_id = query.data.split(':', maxsplit=2)
    offer = await BikeOffer.get_or_none(pk=int(offer_id)).select_related('request', 'client', 'bike', 'bike__model', 'bike__user', 'request__manager')
    if action == 'accept':
        await query.message.edit_reply_markup(None)
        if offer.request.status != RentalRequest.RequestStatuses.NEW or offer.request.selected_offer_id is not None:
            return await query.message.delete()
        offer.status = BikeOffer.OfferStatuses.ACCEPTED
        await offer.save()
        offer.request.selected_offer = offer
        offer.request.status = RentalRequest.RequestStatuses.SELECTED
        await offer.request.save()
        reply_text = replies.get(
            'accepted_offer_reply',
            'Отличный выбор. Менеджер свяжется с тобой в течении 5 минут. Если ты торопишься, нажми "Написать менеджеру"'
        )
        keyboard = keyboards.ChatWithManagerKeyboard(user.language, offer.request.manager)
        await query.message.answer(reply_text, reply_markup=keyboard.markup())

        message_text = replies.get(
            'new_offer_for_manager',
            constants.NEW_MANAGER_OFFER_REPLY
        ).format(offer=offer)
        manager_keyboard = keyboards.ManagerOfferKeyboard(offer.request.manager.language, offer.pk)
        try:
            await dp.bot.send_message(
                offer.request.manager.telegram_id,
                message_text,
                reply_markup=manager_keyboard.markup()
            )
        except Exception as e:
            print(e)

        await states.MainMenuState.not_selected.set()
        reply_text = replies.get(
            'back_simple_client_menu_reply',
            'Ты вернулся в главное меню.'
        ).format(user=user)
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        await query.message.answer(reply_text, reply_markup=keyboard.markup())
        await offer.request.offers.all().exclude(pk=offer.pk).update(status=BikeOffer.OfferStatuses.EXPIRED)
        other_offers = await offer.request.offers.all().exclude(pk=offer.pk).select_related('bike__user', 'client')
        for another_offer in other_offers:
            try:
                await business_bot_dp.bot.delete_message(another_offer.bike.user.telegram_id, another_offer.business_message_id)
            except Exception as e:
                print(e)
            try:
                if another_offer.client_message_id:
                    await dp.bot.delete_message(another_offer.client.telegram_id, another_offer.client_message_id)
            except Exception as e:
                print(e)


@dp.message_handler(state=states.ActiveRequestState.request_id)
async def active_request_message(message: types.Message, user: User, replies: dict[str, str], state: FSMContext, options: dict):
    idr_exchange_rate = float(options.get('idr_per_usd_exchange_rate', 15100))
    button_id = keyboards.RequestCreatedKeyboard.get_button_id_by_text(user.language, message.text)
    state_data = await state.get_data()
    rent_request = await RentalRequest.get_or_none(pk=int(state_data['request_id'])).select_related('manager')
    if button_id == 'rent_another_bike_button_label':
        if not rent_request:
            return
        await rent_request.offers.all().delete()
        rent_request.status = RentalRequest.RequestStatuses.CANCELED
        await rent_request.save()
        await states.RentRequestState.model.set()
        reply_text = replies.get('rent_a_bike_init_reply', 'Заполни заявку на аренду').format(user=user)
        keyboard = keyboards.CancelActionKeyboard(language=user.language)
        await message.answer(reply_text, reply_markup=keyboard.markup())
        reply_text = replies.get('rent_a_bike_reply', 'Какую модель хочешь?').format(user=user)
        models = await BikeModel.all()
        keyboard = keyboards.SelectBikeModelKeyboard(models, user.language, idr_exchange_rate)
        return await message.answer(reply_text, reply_markup=await keyboard.markup())
    elif button_id == 'chat_with_manager_button_label':
        reply_text = replies.get(
            'active_request_chat_with_manager_select_action',
            'Для разговора с менеджером нажми на кнопку'
        ).format(user=user)
        keyboard = keyboards.ChatWithManagerKeyboard(user.language, rent_request.manager)
        await message.answer(reply_text, reply_markup=keyboard.markup())
    else:
        reply_text = replies.get(
            'active_request_state_select_action',
            'Выбери действие из списка'
        ).format(user=user)
        keyboard = keyboards.RequestCreatedKeyboard(user.language)
        await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.ManagerOfferKeyboard.get_regexp()), state='*')
async def handle_manager_response(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, action, offer_id = query.data.split(':', maxsplit=3)
    offer = await BikeOffer.get(pk=int(offer_id)).select_related('request', 'bike')
    if action == 'accept':
        offer.status = BikeOffer.OfferStatuses.COMPLETE
        await offer.save()
        offer.request.status = RentalRequest.RequestStatuses.COMPLETE
        await offer.request.save()
        existing_booking_count = await BikeBooking.filter(offer=offer, bike=offer.bike).count()
        if existing_booking_count > 0:
            await BikeBooking.filter(offer=offer, bike=offer.bike).delete()
        await BikeBooking.create(
            bike=offer.bike,
            offer=offer,
            from_date=offer.request.rent_start_date,
            to_date=offer.request.rent_end_date
        )
    if action == 'reject':
        offer.request.status = RentalRequest.RequestStatuses.CANCELED
        await offer.request.save()
        offer.status = BikeOffer.OfferStatuses.REJECTED
        await offer.save()
    await query.message.edit_reply_markup(None)
