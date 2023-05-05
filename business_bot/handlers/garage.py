from datetime import datetime
from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from loguru import logger

from business_bot import dp, states, keyboards, constants, helpers
from database.models import User, Garage, Bike, BikeBooking
from client_bot import dp as client_dp

@dp.message_handler(state=states.SetupGarageState.owner_name, content_types=types.ContentTypes.TEXT)
async def garage_owner_name_entered(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    await state.update_data(owner_name=message.text)
    await states.SetupGarageState.name.set()
    reply_text = replies.get('enter_garage_name', 'Как называется компания?').format(user=user)
    await message.answer(reply_text)


@dp.message_handler(state=states.SetupGarageState.name, content_types=types.ContentTypes.TEXT)
async def garage_name_entered(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    await state.update_data(name=message.text)
    await states.SetupGarageState.location.set()
    reply_text = replies.get('enter_garage_location', 'Где находится гараж?(Отправьте координаты)').format(user=user)
    await message.answer(reply_text)

@dp.message_handler(state=states.SetupGarageState.location, content_types=types.ContentType.LOCATION)
async def garage_location_received(message: types.Message, user: User, replies: dict[str, str], state: FSMContext):
    data = await state.get_data()
    update = data.get('update', False)
    if not update:
        garage = await Garage.create(
            owner=user,
            name='',
            owner_name='',
            lat=message.location.latitude,
            lon=message.location.longitude
        )
        manager = await User.get_random_manager()
        if manager:
            await client_dp.bot.send_message(
                manager.telegram_id,
                replies.get('new_rental', 'Новый поставщик: @{user.username}').format(user=user)
            )
    else:
        garage = await user.garages.all().first()
        if not garage:
            garage = await Garage.create(
                owner=user,
                lat=message.location.latitude,
                lon=message.location.longitude
            )
        else:
            garage.lat = message.location.latitude
            garage.lon = message.location.longitude
            await garage.save()
    await state.finish()
    await states.MainMenuState.not_selected.set()
    state = dp.current_state()
    await state.update_data(garage_id=garage.pk)
    reply_text = replies.get(
        'setup_garage_succeed',
        'Информация сохранена. Это твой новый виртуальный офис. Начни заполнять гараж!'
    ).format(user=user)
    keyboard = keyboards.MainMenuKeyboard(user.language)
    await message.answer(reply_text, reply_markup=keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.GarageBikesKeyboard.get_regexp()), state=states.GarageState.bikes_list)
async def garage_bikes_button_clicked(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, _, key = query.data.split(':', maxsplit=2)
    if key == 'rent':
        reply_text = replies.get('rent_bikes_reply', 'Байки, которые катают клиентов').format(user=user)
        rent_bike_ids = await BikeBooking.filter(
            bike__user=user,
            from_date__lte=datetime.now(),
            to_date__gte=datetime.now()
        ).values_list('bike_id', flat=True)
        keyboard = keyboards.RentBikesKeyboard(
            Bike.filter(id__in=rent_bike_ids),
            user.language,
            add_back_button=True
        )
        return await query.message.edit_text(reply_text, reply_markup=await keyboard.markup())
    if key == 'available':
        reply_text = replies.get('available_bikes_reply', 'Байки, которые ждут клиентов').format(user=user)
        rent_bike_ids = await BikeBooking.filter(
            bike__user=user,
            from_date__lte=datetime.now(),
            to_date__gte=datetime.now()
        ).values_list('bike_id', flat=True)
        keyboard = keyboards.AvailableBikesKeyboard(
            Bike.filter(user=user).exclude(id__in=rent_bike_ids),
            user.language,
            add_back_button=True
        )
        return await query.message.edit_text(reply_text, reply_markup=await keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.RentBikesKeyboard.get_regexp()), state=states.GarageState.bikes_list)
async def rent_bikes_list_press(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, action, param = query.data.split(':')
    if action == 'pg':
        rent_bike_ids = await BikeBooking.filter(
            bike__user=user,
            from_date__lte=datetime.now(),
            to_date__gte=datetime.now()
        ).values_list('bike_id', flat=True)
        keyboard = keyboards.RentBikesKeyboard(
            Bike.filter(id__in=rent_bike_ids),
            user.language,
            page=int(param),
            add_back_button=True
        )
        return await query.message.edit_reply_markup(await keyboard.markup())
    if action == 'bk':
        reply_text = replies.get('rental_calendar_reply', 'Здесь ты можешь посмотреть доступные байки байки в аренде').format(user=user)
        keyboard = keyboards.GarageBikesKeyboard(user.language)
        return await query.message.edit_text(reply_text, reply_markup=keyboard.markup())
    if action == 'sl':
        bike = await Bike.get_or_none(pk=int(param), user=user).select_related('model')
        if not bike:
            return
        await states.GarageState.bike_details.set()
        state = dp.current_state()
        await state.update_data(list_type='rent')
        caption = replies.get('bike_info_reply', constants.DEFAULT_BIKE_DETAILS_MESSAGE).format(
            bike=bike,
            color=helpers.language.get_translation(user.language, f'{bike.color}_color_label', bike.color),
            abs_support=helpers.language.get_translation(user.language, 'yes', 'Да') if bike.abs else helpers.language.get_translation(user.language, 'no', 'Нет'),
            keyless_support=helpers.language.get_translation(user.language, 'yes', 'Да') if bike.keyless else helpers.language.get_translation(user.language, 'no', 'Нет'),
        )
        photo = await bike.photos.all().first()
        keyboard = keyboards.BikeManagementKeyboard(user.language, bike)
        if photo:
            await query.message.answer_photo(
                photo.telegram_id,
                caption=caption,
                reply_markup=keyboard.markup()
            )
        else:
            await query.message.answer(
                caption,
                reply_markup=keyboard.markup()
            )
        await query.message.delete()


@dp.callback_query_handler(filters.Regexp(keyboards.AvailableBikesKeyboard.get_regexp()), state=states.GarageState.bikes_list)
async def available_bikes_list_press(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, action, param = query.data.split(':')
    if action == 'pg':
        rent_bike_ids = await BikeBooking.filter(
            bike__user=user,
            from_date__lte=datetime.now(),
            to_date__gte=datetime.now()
        ).values_list('bike_id', flat=True)
        keyboard = keyboards.RentBikesKeyboard(
            Bike.filter(user=user).exclude(id__in=rent_bike_ids),
            user.language,
            page=int(param),
            add_back_button=True
        )
        return await query.message.edit_reply_markup(await keyboard.markup())
    if action == 'bk':
        reply_text = replies.get('rental_calendar_reply', 'Здесь ты можешь посмотреть доступные байки байки в аренде').format(user=user)
        keyboard = keyboards.GarageBikesKeyboard(user.language)
        return await query.message.edit_text(reply_text, reply_markup=keyboard.markup())
    if action == 'sl':
        logger.warning('________>__________')
        bike = await Bike.get_or_none(pk=int(param), user=user).select_related('model')
        if not bike:
            return
        await states.GarageState.bike_details.set()
        state = dp.current_state()
        await state.update_data(list_type='available')
        caption = replies.get('bike_info_reply', constants.DEFAULT_BIKE_DETAILS_MESSAGE).format(
            bike=bike,
            color=helpers.language.get_translation(user.language, f'{bike.color}_color_label', bike.color),
            abs_support=helpers.language.get_translation(user.language, 'yes', 'Да') if bike.abs else helpers.language.get_translation(user.language, 'no', 'Нет'),
            keyless_support=helpers.language.get_translation(user.language, 'yes', 'Да') if bike.keyless else helpers.language.get_translation(user.language, 'no', 'Нет'),
        )
        photo = await bike.photos.all().first()
        keyboard = keyboards.BikeManagementKeyboard(user.language, bike)
        if photo:
            await query.message.answer_photo(
                photo.telegram_id,
                caption=caption,
                reply_markup=keyboard.markup()
            )
        else:
            await query.message.answer(
                caption,
                reply_markup=keyboard.markup()
            )
        await query.message.delete()


@dp.callback_query_handler(filters.Regexp(keyboards.BikeManagementKeyboard.get_regexp()), state=states.GarageState.bike_details)
async def bike_details_press(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, action, bike_id = query.data.split(':', maxsplit=2)
    bike = await Bike.get_or_none(pk=bike_id, user=user).select_related('model')
    if action == 'date':
        if not bike:
            return
        reply_text = replies.get(
            'bike_edit_select_availability_date',
            'Укажи дату, когда он сможет поехать к клиенту.'
        ).format(user=user)
        await state.update_data(bike_id=int(bike_id))
        await states.BikeState.availability_date.set()
        keyboard = keyboards.BikeAvailabilityKeyboard(language=user.language)
        await query.message.answer(reply_text, reply_markup=keyboard.markup())
        await query.message.delete()
    if action == 'edit':
        if not bike:
            return
        old_state = await state.get_data()
        await states.BikeState.year.set()
        state = dp.current_state()
        await state.update_data(bike_id=int(bike_id), model=bike.model.pk, model_name=bike.model.name, list_type=old_state.get('list_type'))
        reply_text = replies.get('edit_bike_start', 'Заполни новые данные байка').format(user=user)
        keyboard = keyboards.CancelActionKeyboard(language=user.language)
        await query.message.answer(reply_text, reply_markup=keyboard.markup())
        reply_text = replies.get('enter_bike_year', 'Какой год выпуска байка?').format(user=user)
        await query.message.answer(reply_text)
        await query.message.delete()
    if action == 'delete':
        if not bike:
            return
        reply_text = replies.get('confirm_bike_deletion', 'Вы уверены что хотите удалить байк?').format(user=user)
        keyboard = keyboards.ConfirmBikeDeletionKeyboard(language=user.language, bike_id=int(bike_id))
        await query.message.answer(reply_text, reply_markup=keyboard.markup())
        await query.message.delete()
    if action == 'list':
        state_data = await state.get_data()
        print(state_data)
        await states.GarageState.bikes_list.set()
        state = dp.current_state()
        if state_data.get('list_type') == 'available':
            reply_text = replies.get('available_bikes_reply', 'Байки, которые ждут клиентов').format(user=user)
            rent_bike_ids = await BikeBooking.filter(
                bike__user=user,
                from_date__lte=datetime.now(),
                to_date__gte=datetime.now()
            ).values_list('bike_id', flat=True)
            keyboard = keyboards.AvailableBikesKeyboard(
                Bike.filter(user=user).exclude(id__in=rent_bike_ids),
                user.language,
                add_back_button=True
            )
        if state_data.get('list_type') == 'rent':
            reply_text = replies.get('rent_bikes_reply', 'Байки, которые катают клиентов').format(user=user)
            rent_bike_ids = await BikeBooking.filter(
                bike__user=user,
                from_date__lte=datetime.now(),
                to_date__gte=datetime.now()
            ).values_list('bike_id', flat=True)
            keyboard = keyboards.RentBikesKeyboard(
                Bike.filter(id__in=rent_bike_ids),
                user.language,
                add_back_button=True
            )
        await query.message.delete()
        await query.message.answer(reply_text, reply_markup=await keyboard.markup())


@dp.callback_query_handler(filters.Regexp(keyboards.ConfirmBikeDeletionKeyboard.get_regexp()), state=states.GarageState.bike_details)
async def bike_deletion(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext):
    _, action, bike_id = query.data.split(':', maxsplit=2)
    bike = await Bike.get_or_none(pk=int(bike_id), user=user).select_related('model')
    if not bike:
        await states.MainMenuState.not_selected.set()
        reply_text = replies.get(
            'main_menu_reply',
            'Ты находишься в офисе. Выбери нужное действие из списка'
        ).format(user=user)
        keyboard = keyboards.MainMenuKeyboard(user.language)
        await query.message.answer(reply_text, reply_markup=keyboard.markup())
        await query.message.delete()
        return
    if action == 'confirm':
        await bike.delete()
        reply_text = replies.get('bike_deleted_reply', 'Байк удален').format(user=user)
        await query.message.edit_text(reply_text, reply_markup=None)
        state_data = await state.get_data()
        await states.GarageState.bikes_list.set()
        state = dp.current_state()
        if state_data.get('list_type') == 'available':
            reply_text = replies.get('available_bikes_reply', 'Байки, которые ждут клиентов').format(user=user)
            await state.update_data(list_type='available')
            rent_bike_ids = await BikeBooking.filter(
                bike__user=user,
                from_date__lte=datetime.now(),
                to_date__gte=datetime.now()
            ).values_list('bike_id', flat=True)
            keyboard = keyboards.AvailableBikesKeyboard(
                Bike.filter(user=user).exclude(id__in=rent_bike_ids),
                user.language,
                add_back_button=True
            )
        if state_data.get('list_type') == 'rent':
            reply_text = replies.get('rent_bikes_reply', 'Байки, которые катают клиентов').format(user=user)
            await state.update_data(list_type='rent')
            rent_bike_ids = await BikeBooking.filter(
                bike__user=user,
                from_date__lte=datetime.now(),
                to_date__gte=datetime.now()
            ).values_list('bike_id', flat=True)
            keyboard = keyboards.RentBikesKeyboard(
                Bike.filter(id__in=rent_bike_ids),
                user.language,
                add_back_button=True
            )
        await query.message.answer(reply_text, reply_markup=await keyboard.markup())
        return await query.message.delete()
    if action == 'cancel':
        caption = replies.get('bike_info_reply', constants.DEFAULT_BIKE_DETAILS_MESSAGE).format(
            bike=bike,
            color=helpers.language.get_translation(user.language, f'{bike.color}_color_label', bike.color),
            abs_support=helpers.language.get_translation(user.language, 'yes', 'Да') if bike.abs else helpers.language.get_translation(user.language, 'no', 'Нет'),
            keyless_support=helpers.language.get_translation(user.language, 'yes', 'Да') if bike.keyless else helpers.language.get_translation(user.language, 'no', 'Нет'),
        )
        photo = await bike.photos.all().first()
        keyboard = keyboards.BikeManagementKeyboard(user.language, bike)
        if photo:
            await query.message.answer_photo(
                photo.telegram_id,
                caption=caption,
                reply_markup=keyboard.markup()
            )
        else:
            await query.message.answer(
                caption,
                reply_markup=keyboard.markup()
            )
        return await query.message.delete()
