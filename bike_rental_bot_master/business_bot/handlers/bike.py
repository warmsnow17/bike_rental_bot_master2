from decimal import Decimal
from datetime import datetime, timedelta
from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from business_bot import dp, states, keyboards, helpers, constants
from database.models import User, BikeModel, Bike, BikePhoto, BikeBooking


async def process_cancel(state: FSMContext, replies: dict, user: User, message: types.Message):
    state_data = await state.get_data()
    await state.finish()
    if state_data.get('list_type'):
        reply_text = replies.get(
            'back_main_menu_reply',
            'Действие отменено.'
        ).format(user=user)
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        await message.answer(reply_text, reply_markup=keyboard.markup())
        await states.GarageState.bike_details.set()
        state = dp.current_state()
        await state.update_data(list_type=state_data.get('list_type'))
        bike = await Bike.get_or_none(pk=state_data.get('bike_id')).select_related('model')
        if not bike:
            return
        caption = replies.get('bike_info_reply', constants.DEFAULT_BIKE_DETAILS_MESSAGE).format(
            bike=bike,
            color=helpers.language.get_translation(
                user.language,
                f'{bike.color}_color_label',
                bike.color
            ),
            abs_support=helpers.language.get_translation(user.language, 'yes', 'Да') if bike.abs else helpers.language.get_translation(user.language, 'no', 'Нет'),
            keyless_support=helpers.language.get_translation(user.language, 'yes', 'Да') if bike.keyless else helpers.language.get_translation(user.language, 'no', 'Нет'),
        )
        photo = await bike.photos.all().first()
        keyboard = keyboards.BikeManagementKeyboard(user.language, bike)
        if photo:
            await message.answer_photo(
                photo.telegram_id,
                caption=caption,
                reply_markup=keyboard.markup()
            )
        else:
            await message.answer(
                caption,
                reply_markup=keyboard.markup()
            )
        return
    reply_text = replies.get(
        'back_main_menu_reply',
        'Действие отменено. Вы вернулись в виртуальный офис.'
    ).format(user=user)
    await states.MainMenuState.not_selected.set()
    keyboard = keyboards.MainMenuKeyboard(language=user.language)
    return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.SelectBikeModelKeyboard.get_regexp()), state=states.BikeState.model)
async def bike_model_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, model_id = query.data.split(':', maxsplit=2)
    model = await BikeModel.get_or_none(pk=int(model_id))
    await state.update_data(model=model_id, model_name=model.name if model else '')
    new_message_text = replies.get('bike_model_selected', 'Выбрана модель: {model.name}').format(model=model)
    await query.message.edit_text(new_message_text, reply_markup=None)
    reply_text = replies.get('enter_bike_year', 'Какой год выпуска байка?').format(user=user)
    await states.BikeState.year.set()
    return await query.message.answer(reply_text)


@dp.message_handler(state=states.BikeState.model)
async def wrong_bike_model(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        return await process_cancel(state, replies, user, message)
    reply_text = replies.get('select_bike_model_warning', 'Выбери модель байка').format(user=user)
    await message.answer(reply_text)


@dp.message_handler(state=states.BikeState.year)
async def year_entered(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
       return await process_cancel(state, replies, user, message)
    try:
        year = int(message.text)
    except:
        reply_text = replies.get('bike_year_warning', 'Введи год выпуска').format(user=user)
        return await message.answer(reply_text)
    if year < 1800 or year > datetime.now().year:
        reply_text = replies.get('bike_year_warning', 'Введи год выпуска').format(user=user)
        return await message.answer(reply_text)
    await state.update_data(year=year)
    await states.BikeState.mileage.set()
    reply_text = replies.get('enter_bike_mileage', 'Какой пробег у байка?').format(user=user)
    return await message.answer(reply_text)


@dp.message_handler(state=states.BikeState.mileage)
async def mileage_entered(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        return await process_cancel(state, replies, user, message)
    try:
        mileage = int(message.text)
    except:
        reply_text = replies.get('bike_mileage_warning', 'Введи пробег').format(user=user)
        return await message.answer(reply_text)
    if mileage < 0:
        reply_text = replies.get('bike_mileage_warning', 'Введи пробег').format(user=user)
        return await message.answer(reply_text)
    await state.update_data(mileage=mileage)
    await states.BikeState.color.set()
    reply_text = replies.get('select_bike_color', 'Какого цвета байк?').format(user=user)
    colors = [
        {'key': 'bright', 'value': helpers.language.get_translation(user.language, 'bright_color_label', 'Яркий')},
        {'key': 'white', 'value': helpers.language.get_translation(user.language, 'white_color_label', 'Белый')},
        {'key': 'red', 'value': helpers.language.get_translation(user.language, 'red_color_label', 'Красный')},
        {'key': 'black', 'value': helpers.language.get_translation(user.language, 'black_color_label', 'Черный')},
        {'key': 'blue', 'value': helpers.language.get_translation(user.language, 'blue_color_label', 'Синий')},
        {'key': 'yellow', 'value': helpers.language.get_translation(user.language, 'yellow_color_label', 'Желтый')},
        {'key': 'other', 'value': helpers.language.get_translation(user.language, 'other_color_label', 'Другой')},
    ]
    keyboard = keyboards.SelectBikeColorKeyboard(colors)
    return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.SelectBikeColorKeyboard.get_regexp()), state=states.BikeState.color)
async def bike_color_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, color = query.data.split(':', maxsplit=2)
    if color == 'other':
        await states.BikeState.manual_color.set()
        return await query.message.edit_text(replies.get('enter_bike_color', 'Введи цвет байка'), reply_markup=None)
    color_name = helpers.language.get_translation(user.language, f'{color}_color_label', color)
    await state.update_data(color=color, color_name=color_name)
    new_text = replies.get('selected_color', 'Цвет: {color_name}').format(color_name=color_name)
    await query.message.edit_text(new_text, reply_markup=None)
    await states.BikeState.abs.set()
    reply_text = replies.get('select_bike_abs_support', 'Байк с ABS?').format(user=user)
    keyboard = keyboards.SelectBikeAbsKeyboard(language=user.language)
    return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.BikeState.manual_color)
async def bike_color_entered(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    await state.update_data(color=message.text, color_name=message.text)
    await states.BikeState.abs.set()
    reply_text = replies.get('select_bike_abs_support', 'Байк с ABS?').format(user=user)
    keyboard = keyboards.SelectBikeAbsKeyboard(language=user.language)
    return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.BikeState.color)
async def wrong_bike_color(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        return await process_cancel(state, replies, user, message)
    reply_text = replies.get('select_bike_color_warning', 'Выбери цвет байка').format(user=user)
    return await message.answer(reply_text)


@dp.callback_query_handler(filters.Regexp(keyboards.SelectBikeAbsKeyboard.get_regexp()), state=states.BikeState.abs)
async def bike_abs_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, abs_support = query.data.split(':', maxsplit=2)
    if abs_support == 'yes':
        await state.update_data(abs=True, abs_label=helpers.language.get_translation(user.language, 'yes', 'Да'))
        await query.message.edit_text(replies.get('bike_abs_supported', 'Байк с ABS'), reply_markup=None)
    else:
        await state.update_data(abs=False, abs_label=helpers.language.get_translation(user.language, 'no', 'Нет'))
        await query.message.edit_text(replies.get('bike_abs_not_supported', 'Байк без ABS'), reply_markup=None)
    await states.BikeState.keyless.set()
    reply_text = replies.get('select_bike_keyless_support', 'Байк с Keyless доступом?').format(user=user)
    keyboard = keyboards.SelectBikeKeylessKeyboard(language=user.language)
    return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.BikeState.abs)
async def wrong_bike_abs(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        return await process_cancel(state, replies, user, message)
    reply_text = replies.get('select_bike_abs_warning', 'Укажи наличие ABS у байка').format(user=user)
    return await message.answer(reply_text)


@dp.callback_query_handler(filters.Regexp(keyboards.SelectBikeKeylessKeyboard.get_regexp()), state=states.BikeState.keyless)
async def bike_keyless_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, keyless_support = query.data.split(':', maxsplit=2)
    if keyless_support == 'yes':
        await state.update_data(keyless=True, keyless_label=helpers.language.get_translation(user.language, 'yes', 'Да'))
        await query.message.edit_text(replies.get('bike_keyless_supported', 'Байк с Keyless'), reply_markup=None)
    else:
        await state.update_data(keyless=False, keyless_label=helpers.language.get_translation(user.language, 'no', 'Нет'))
        await query.message.edit_text(replies.get('bike_keyless_not_supported', 'Байк без Keyless'), reply_markup=None)
    await states.BikeState.number.set()
    reply_text = replies.get('enter_bike_number', 'Введи гос. номер байка').format(user=user)
    return await query.message.answer(reply_text)


@dp.message_handler(state=states.BikeState.keyless)
async def wrong_bike_keyless(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        return await process_cancel(state, replies, user, message)
    reply_text = replies.get('select_bike_keyless_warning', 'Укажи наличие Keyless доступа у байка').format(user=user)
    return await message.answer(reply_text)


@dp.message_handler(state=states.BikeState.number)
async def bike_number(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        return await process_cancel(state, replies, user, message)
    await state.update_data(number=message.text)
    await states.BikeState.price.set()
    reply_text = replies.get('enter_bike_price', 'Введи цену аренды за сутки').format(user=user)
    return await message.answer(reply_text)


@dp.message_handler(state=states.BikeState.price)
async def bike_price(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        return await process_cancel(state, replies, user, message)
    try:
        price = Decimal(message.text)
    except:
        reply_text = replies.get('bike_price_warning', 'Введи цену аренды за сутки').format(user=user)
        return await message.answer(reply_text)
    await state.update_data(price=price)
    await states.BikeState.weekly_price.set()
    reply_text = replies.get('enter_bike_weekly_price', 'Введи цену аренды за неделю').format(user=user)
    return await message.answer(reply_text)


@dp.message_handler(state=states.BikeState.weekly_price)
async def bike_weekly_price(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        return await process_cancel(state, replies, user, message)
    try:
        price = Decimal(message.text)
    except:
        reply_text = replies.get('bike_weekly_price_warning', 'Введи цену аренды за неделю').format(user=user)
        return await message.answer(reply_text)
    await state.update_data(weekly_price=price)
    await states.BikeState.biweekly_price.set()
    reply_text = replies.get('enter_bike_biweekly_price', 'Введи цену аренды за две недели').format(user=user)
    return await message.answer(reply_text)


@dp.message_handler(state=states.BikeState.biweekly_price)
async def bike_biweekly_price(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        return await process_cancel(state, replies, user, message)
    try:
        price = Decimal(message.text)
    except:
        reply_text = replies.get('bike_biweekly_price_warning', 'Введи цену аренды за две недели').format(user=user)
        return await message.answer(reply_text)
    await state.update_data(biweekly_price=price)
    await states.BikeState.threeweekly_price.set()
    reply_text = replies.get('enter_bike_threeweekly_price', 'Введи цену аренды за три недели').format(user=user)
    return await message.answer(reply_text)


@dp.message_handler(state=states.BikeState.threeweekly_price)
async def bike_threeweekly_price(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        return await process_cancel(state, replies, user, message)
    try:
        price = Decimal(message.text)
    except:
        reply_text = replies.get('bike_threeweekly_price_warning', 'Введи цену аренды за три недели').format(user=user)
        return await message.answer(reply_text)
    await state.update_data(threeweekly_price=price)
    await states.BikeState.monthly_price.set()
    reply_text = replies.get('enter_bike_monthly_price', 'Введи цену аренды за месяц').format(user=user)
    return await message.answer(reply_text)


@dp.message_handler(state=states.BikeState.monthly_price)
async def bike_monthly_price(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        return await process_cancel(state, replies, user, message)
    try:
        price = Decimal(message.text)
    except:
        reply_text = replies.get('bike_monthly_price_warning', 'Введи цену аренды за месяц').format(user=user)
        return await message.answer(reply_text)
    await state.update_data(monthly_price=price)
    await states.BikeState.bimonthly_price.set()
    reply_text = replies.get('enter_bike_bimonthly_price', 'Введи цену аренды за два месяца и более').format(user=user)
    return await message.answer(reply_text)


@dp.message_handler(state=states.BikeState.bimonthly_price)
async def bike_bimonthly_price(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.CancelActionKeyboard.is_cancel_message(user.language, message.text):
        return await process_cancel(state, replies, user, message)
    try:
        price = Decimal(message.text)
    except:
        reply_text = replies.get('bike_bimonthly_price_warning', 'Введи цену аренды за два месяца и более').format(user=user)
        return await message.answer(reply_text)
    await state.update_data(bimonthly_price=price)
    await states.BikeState.photos.set()
    reply_text = replies.get('send_bike_photos', 'Отправь фотографию байка').format(user=user)
    return await message.answer(reply_text)


@dp.message_handler(state=states.BikeState.photos, content_types=types.ContentType.TEXT)
async def bike_photo_text(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    if keyboards.DoneCancelKeyboard.is_cancel_message(user.language, message.text):
        return await process_cancel(state, replies, user, message)
    reply_text = replies.get('not_photo_warning', 'Отправь фотографию').format(user=user)
    return await message.answer(reply_text)


@dp.message_handler(state=states.BikeState.photos, content_types=types.ContentType.PHOTO)
async def bike_photo(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    bike_data = await state.get_data()
    photos = bike_data.get('photos', [])
    photos.append(message.photo[-1].file_id)
    await state.update_data(photos=photos)
    await states.BikeState.review.set()
    reply_text = replies.get('review_bike', constants.DEFAULT_REVIEW_MESSAGE).format(user=user, **bike_data)
    keyboard = keyboards.BikeConfirmationKeyboard(language=user.language)
    return await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.message_handler(state=states.BikeState.review)
async def review_message(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    reply_text = replies.get('review_bike_warning', 'Подтверди информацию о байке').format(user=user)
    return await message.answer(reply_text)


@dp.callback_query_handler(state=states.BikeState.review)
async def review_message(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, answer = query.data.split(':', maxsplit=2)
    if answer == 'yes':
        bike_data = await state.get_data()
        bike_id = bike_data.get('bike_id', None)
        if bike_id:
            bike = await Bike.get_or_none(pk=bike_id)
            if not bike:
                return
            bike.model = await BikeModel.get(pk=bike_data['model'])
            if 'year' in bike_data:
                bike.year = bike_data['year']
            if 'mileage' in bike_data:
                bike.mileage = bike_data['mileage']
            if 'color' in bike_data:
                bike.color = bike_data['color']
            if 'abs' in bike_data:
                bike.abs = bike_data['abs']
            if 'keyless' in bike_data:
                bike.keyless = bike_data['keyless']
            if 'number' in bike_data:
                bike.number = bike_data['number']
            if 'price' in bike_data:
                bike.price = bike_data['price']
            if 'weekly_price' in bike_data:
                bike.weekly_price = bike_data['weekly_price']
            if 'biweekly_price' in bike_data:
                bike.biweekly_price = bike_data['biweekly_price']
            if 'threeweekly_price' in bike_data:
                bike.threeweekly_price = bike_data['threeweekly_price']
            if 'monthly_price' in bike_data:
                bike.monthly_price = bike_data['monthly_price']
            if 'bimonthly_price' in bike_data:
                bike.bimonthly_price = bike_data['bimonthly_price']
            await bike.save()
            await bike.photos.all().delete()
        else:
            model = await BikeModel.get_or_none(pk=int(bike_data['model']))
            if model:
                bike = await Bike.create(
                    user=user,
                    model=model,
                    year=bike_data['year'],
                    mileage=bike_data['mileage'],
                    color=bike_data['color'],
                    abs=bike_data['abs'],
                    keyless=bike_data['keyless'],
                    number=bike_data['number'],
                    price=bike_data['price'],
                    weekly_price=bike_data['weekly_price'],
                    biweekly_price=bike_data['biweekly_price'],
                    threeweekly_price=bike_data['threeweekly_price'],
                    monthly_price=bike_data['monthly_price'],
                    bimonthly_price=bike_data['bimonthly_price']
                )
        for photo in bike_data['photos']:
            await BikePhoto.create(
                bike=bike,
                telegram_id=photo
            )
        await query.message.edit_reply_markup(None)
        if not bike_id:
            reply_text = replies.get(
                'bike_added_select_availability_date',
                'Отлично! Теперь укажи дату, когда он сможет поехать к клиенту.'
            ).format(user=user)
            await state.update_data(bike_id=bike.pk)
            await states.BikeState.availability_date.set()
            keyboard = keyboards.BikeAvailabilityKeyboard(language=user.language)
            return await query.message.answer(reply_text, reply_markup=keyboard.markup())
        else:
            reply_text = replies.get(
                'bike_updated_switched_to_main_menu',
                'Информация обновлена. Вы вернулись в виртуальный офис.'
            ).format(user=user)
            await states.MainMenuState.not_selected.set()
            keyboard = keyboards.MainMenuKeyboard(language=user.language)
            return await query.message.answer(reply_text, reply_markup=keyboard.markup())
    if answer == 'no':
        await states.BikeState.model.set()
        reply_text = replies.get('bike_state_initial', 'Нужно заново ответить на вопросы').format(user=user)
        keyboard = keyboards.CancelActionKeyboard(language=user.language)
        await query.message.answer(reply_text, reply_markup=keyboard.markup())
        reply_text = replies.get('select_bike_model', 'Какая модель байка?').format(user=user)
        bike_models = await BikeModel.all()
        keyboard = keyboards.SelectBikeModelKeyboard(bike_models)
        return await query.message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.BikeAvailabilityKeyboard.get_regexp()), state=states.BikeState.availability_date)
async def availability_date_selected(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, action, params = query.data.split(':', maxsplit=2)
    if action == 'sw':
        year, month, day = params.split(':')
        keyboard = keyboards.BikeAvailabilityKeyboard(user.language, int(month), int(year))
        return await query.message.edit_reply_markup(keyboard.markup())
    if action == 'sl':
        bike_data = await state.get_data()
        bike = await Bike.get_or_none(pk=bike_data.get('bike_id'))
        if not bike:
            return
        year, month, day = params.split(':')
        availability_date = datetime(int(year), int(month), int(day), 0, 0, 0, 0)
        bike.rental_start_date = availability_date
        await bike.save()
        await state.finish()
        reply_text = replies.get('selected_availability_date_reply', 'Байк будет доступен {date}').format(
            user=user,
            date=availability_date.strftime('%d.%m.%Y')
        )
        await query.message.edit_text(reply_text, reply_markup=None)
        reply_text = replies.get(
            'bike_added_switched_to_main_menu',
            'Отлично! Твой байк готов к аренде. Тебе придет сообщение с информацией о новом заказе.'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await query.message.answer(reply_text, reply_markup=keyboard.markup())
