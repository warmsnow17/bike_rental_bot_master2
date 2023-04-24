from datetime import datetime, timedelta
from aiogram import types, filters
from aiogram.dispatcher import FSMContext
from business_bot import dp, states, keyboards, constants, helpers
from client_bot import keyboards as client_keyboards, dp as client_dp
from database.models import User, BikeOffer, RentalRequest


@dp.callback_query_handler(filters.Regexp(client_keyboards.NewBikeRentRequestKeyboard.get_regexp()), state='*')
async def answer_client_offer(query: types.CallbackQuery, user: User, replies: dict[str, str], state: FSMContext, options: dict[str, str]):
    _, action, offer_id = query.data.split(':', maxsplit=2)
    idr_exchange_rate = float(options.get('idr_per_usd_exchange_rate', 15100))
    offer = await BikeOffer.get_or_none(pk=int(offer_id)).select_related('bike', 'client', 'request', 'bike__model')
    if not offer:
        reply_text = replies.get('request_not_available', 'Уже не актуально')
        return await query.message.edit_text(reply_text, reply_markup=None)
    confirmed_offers_count = await offer.request.offers.filter(status=BikeOffer.OfferStatuses.CONFIRMED).count()
    offer_date = datetime.now() - timedelta(minutes=int(options.get('bike_request_lifetime', 5)))
    if offer.request.created_at < offer_date.astimezone():
        reply_text = replies.get('request_not_available', 'Уже не актуально')
        return await query.message.edit_text(reply_text, reply_markup=None)
    if offer.request.status != RentalRequest.RequestStatuses.NEW or confirmed_offers_count > int(options.get('max_confirmed_offers', 5)):
        reply_text = replies.get('request_not_available', 'Уже не актуально')
        return await query.message.edit_text(reply_text, reply_markup=None)
    if action == 'cancel':
        reply_text = replies.get('offer_select_availability_date', 'Выбери дату когда байк будет доступен')
        keyboard = keyboards.BikeAvailabilityKeyboard(user.language)
        offer.status = BikeOffer.OfferStatuses.REJECTED
        await offer.save()
        await states.BikeState.availability_date.set()
        state = dp.current_state()
        await state.update_data(bike_id=offer.bike.pk)
        return await query.message.edit_text(reply_text, reply_markup=keyboard.markup())
    if action == 'confirm':
        reply_text = replies.get('confirmed_offer_reply_for_business', 'Спасибо! Уточню детали у клиента и вернусь позже').format(user=user)
        await query.message.edit_text(reply_text, reply_markup=None)
        offer.status = BikeOffer.OfferStatuses.CONFIRMED
        await offer.save()

        reply_text = replies.get('confirmed_offer_reply_for_client', constants.DEFAULT_BIKE_OFFER_MESSAGE).format(
            offer=offer,
            bike=offer.bike,
            color=helpers.language.get_translation(
                offer.client.language,
                f'{offer.bike.color}_color_label',
                offer.bike.color
            ),
            abs_support=helpers.language.get_translation(
                offer.client.language,
                'yes_button_label', 'Да'
            ) if offer.bike.abs else helpers.language.get_translation(user.language, 'no_button_label', 'Нет'),
            keyless_support=helpers.language.get_translation(
                offer.client.language,
                'yes_button_label', 'Да'
            ) if offer.bike.keyless else helpers.language.get_translation(user.language, 'no_button_label', 'Нет'),
            usd_price=round(float(offer.price_with_fee) / 1000),
            usd_total_sum=round(float(offer.total_sum_with_fee) / 1000)
        )
        keyboard = client_keyboards.AcceptOfferKeyboard(offer.client.language, offer_id=offer.pk)
        photos = await offer.bike.photos.all()
        if len(photos) > 0:
            file_content = await dp.bot.download_file_by_id(photos[0].telegram_id)
            message = await client_dp.bot.send_photo(
                offer.client.telegram_id,
                file_content,
                caption=reply_text,
                reply_markup=keyboard.markup()
            )
        else:
            message = await client_dp.bot.send_message(
                offer.client.telegram_id,
                reply_text,
                reply_markup=keyboard.markup()
            )
        offer.client_message_id = message.message_id
        await offer.save()
        reply_text = replies.get(
            'switched_to_main_menu',
            'Ты вернулся в виртуальный офис'
        ).format(user=user)
        await states.MainMenuState.not_selected.set()
        keyboard = keyboards.MainMenuKeyboard(language=user.language)
        return await query.message.answer(reply_text, reply_markup=keyboard.markup())
