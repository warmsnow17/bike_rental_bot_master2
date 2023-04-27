TRANSLATIONS = {
    'ru': {
        'rent_a_bike_button_label': 'Хочу арендовать байк',
        'model_help_button_label': 'Помоги с выбором скутера',
        'select_language_button_label': 'Выбрать язык',
        'confirm_button_label': 'Подтверждаю',
        'cancel_button_label': 'Отмена',
        'yes_button_label': 'Да',
        'no_button_label': 'Нет',
        'any_button_label': 'Неважно',
        'day_button_label': 'Сутки',
        'week_button_label': 'неделя',
        'month_button_label': 'Месяц',
        'year_from': 'От',
        'from_label': 'От',
        'any_color_label': 'Любой',
        'daily_rent_label': 'На один/несколько дней',
        'weekly_rent_label': 'От недели до месяца',
        'monthly_rent_label': 'Более месяца',
        'daily_rent_period_label': 'День/Дня/Дней',
        'weekly_rent_period_label': 'Неделю/Недели/Недель',
        'monthly_rent_period_label': 'Месяц/Месяца/Месяцев',
        'rent_another_bike_button_label': 'Я хочу другой байк',
        'chat_with_manager_button_label': 'Чат с менеджером',
        'month_01': 'Январь',
        'month_02': 'Февраль',
        'month_03': 'Март',
        'month_04': 'Апрель',
        'month_05': 'Май',
        'month_06': 'Июнь',
        'month_07': 'Июль',
        'month_08': 'Август',
        'month_09': 'Сентябрь',
        'month_10': 'Октябрь',
        'month_11': 'Ноябрь',
        'month_12': 'Декабрь',
        'week_mo': 'Пн',
        'week_tu': 'Вт',
        'week_we': 'Ср',
        'week_th': 'Чт',
        'week_fr': 'Пт',
        'week_sa': 'Сб',
        'week_su': 'Вс',
        'bright_color_label': 'Яркий',
        'white_color_label': 'Белый',
        'red_color_label': 'Красный',
        'black_color_label': 'Черный',
        'blue_color_label': 'Синий',
        'yellow_color_label': 'Желтый',
        'request_yes_answer_label': 'Нужен',
        'request_no_answer_label': 'Ненужен',
        'request_any_answer_label': 'Неважно',
        'one_helmet_label': 'Один шлем',
        'two_helmets_label': 'Два шлема',
        'no_helmets_label': 'Шлемы не нужны',
        'daily_rent_type_amount_label': 'дней',
        'weekly_rent_type_amount_label': 'недель',
        'monthly_rent_type_amount_label': 'месяцев',
        'accept_offer': 'Хочу этот байк'
    },
    'en': {
        'rent_a_bike_button_label': 'Rent a Scooter',
        'model_help_button_label': 'Help me to choice scooter model',
        'select_language_button_label': 'Select Language',
        'confirm_button_label': 'Confirm',
        'cancel_button_label': 'Cancel',
        'yes_button_label': 'Yes',
        'no_button_label': 'No',
        'any_button_label': 'Doesnt matter',
        'day_button_label': 'Day',
        'week_button_label': 'Week',
        'month_button_label': 'Month',
        'year_from': 'From',
        'from_label': 'From',
        'any_color_label': 'Any',
        'daily_rent_label': 'From day to week',
        'weekly_rent_label': 'From week to month',
        'monthly_rent_label': 'From month',
        'daily_rent_period_label': 'Day(s)',
        'weekly_rent_period_label': 'Week(s)',
        'monthly_rent_period_label': 'Month(s)',
        'rent_another_bike_button_label': 'Rent another bike',
        'chat_with_manager_button_label': 'Chat with manager',
        'month_01': 'January',
        'month_02': 'February',
        'month_03': 'March',
        'month_04': 'April',
        'month_05': 'May',
        'month_06': 'June',
        'month_07': 'July',
        'month_08': 'August',
        'month_09': 'September',
        'month_10': 'October',
        'month_11': 'November',
        'month_12': 'December',
        'week_mo': 'Mo',
        'week_tu': 'Tu',
        'week_we': 'We',
        'week_th': 'Th',
        'week_fr': 'Fr',
        'week_sa': 'Sa',
        'week_su': 'Su',
        'bright_color_label': 'Bright',
        'white_color_label': 'White',
        'red_color_label': 'Red',
        'black_color_label': 'Black',
        'blue_color_label': 'Blue',
        'yellow_color_label': 'Yellow',
        'any_color_label': 'Any',
        'request_yes_answer_label': 'Required',
        'request_no_answer_label': 'Not required',
        'request_any_answer_label': 'Doesnt matter',
        'one_helmet_label': 'One helmet',
        'two_helmets_label': 'Two helmets',
        'no_helmets_label': 'No helmets',
        'daily_rent_type_amount_label': 'days',
        'weekly_rent_type_amount_label': 'weeks',
        'monthly_rent_type_amount_label': 'months',
        'accept_offer': 'Select this one'
    }
}

NEW_MANAGER_OFFER_REPLY = """
Подтверждение по заявке {offer.request.pk}
Клиент: @{offer.client.username}
Выбранный язык: {offer.client.language}
Байк: {offer.bike.model.name}
Поставщик: @{offer.bike.user.username}
Срок аренды: {offer.request.rent_amount} дней
Цена: {offer.price} IDR
Стоимость: {offer.total_sum} IDR
Дата: {offer.request.created_at_date}
"""

ORDER_CONFIRMATION = """Остался последний шаг!
Проверь свой заказ и нажми на кнопку “Подтверждить” 

Модель скутера: {model_obj.name}
Год выпуска: от {year}
Цвет: {color_label}
Бесключевой доступ: {keyless_label}
ABS: {abs_label}
Сколько шлемов нужно: {helmets_label}
Дата начала аренды: {rent_start_date}
Дата возвращения байка: {rent_end_date}
Геопозиция: {lat} {lon}
"""

SIMPLE_ORDER_CONFIRMATION = """Остался последний шаг!
Проверь свой заказ и нажми на кнопку “Подтверждить” 

Модель скутера: {model_obj.name}
Сколько шлемов нужно: {helmets_label}
Вид аренды: {rent_type_label}
Дата начала аренды: {rent_start_date}
Дата возвращения байка: {rent_end_date}
Геопозиция: {lat} {lon}
"""

ORDER_CONFIRMATION_EN = """One last step!
Check your order and click the "Confirm" button 

Scooter Model: {model_obj.name}
Year: from {year}
Colour: {color_label}
Keyless access: {keyless_label}
ABS: {abs_label}
How many helmets are required: {helmets_label}
Rental start date: {rent_start_date}
Bike return date: {rent_end_date}
Геопозиция: {lat} {lon}
"""

SIMPLE_ORDER_CONFIRMATION_EN = """One last step!
Check your order and click the "Confirm" button 

Scooter Model: {model_obj.name}
How many helmets are required: {helmets_label}
Вид аренды: {rent_type_label}
Rental start date: {rent_start_date}
Bike return date: {rent_end_date}
Geo-position: {lat} {lon}
"""

HELP_MESSAGE_TEXT = """Если ты недавно освоил байк и нужна возможность ездить вдвоем – бери Yamaha NMax или Honda PCX. Это почти идентичные модели, главная разница в дизайне.

Honda Scoopy – отличный вариант, если ты хочешь найти самый недорогой скутер или если твой рост до 170см. Он самый компактный и легкий, на нем проще всего учиться.

Если хочешь недорогой, но немного больше и шустрее, чем Scoopy – бери Honda Vario или Yamaha Lexi, еще чуть больше чем Vario.

Если ты уже давно ездишь на скутерах (и на максискутерах тоже), и ты планируешь много длинных поездок, в том числе вдвоем – твой выбор Yamaha Xmax, один из самых больших скутеров в Индонезии.

Какую модель выбираешь?"""

HELP_MESSAGE_TEXT_EN = """If you have recently mastered the bike and need to be able to ride in pairs, take the Yamaha NMax or Honda PCX. These are almost identical models, the main difference being the design.

The Honda Scoopy is a good option if you are looking for the cheapest scooter or if you are up to 170cm tall. It's the most compact and lightweight, and the easiest to learn on.

If you want cheap but a little bigger and faster than the Scoopy, try the Honda Vario or the Yamaha Lexi, which is slightly bigger than the Vario.

If you've been riding scooters for a while (including maxi scooters) and plan to do a lot of long rides, including two - your choice is the Yamaha Xmax, one of the biggest scooters in Indonesia.

Which model do you choose?"""

WELCOME_MESSAGE_TEXT = {
    'ru': """Привет и добро пожаловать! Укажи, какой байк ты хочешь и я свяжусь с сервисом проката, уточню, доступен ли интересующий байк. Далее согласую сроки и цену аренды и предложу тебе несколько доступных вариантов. Если тебя все устроит я подключу менеджера для оформления сделки. """,
    'en': """Hello and welcome! Tell me which bike you want and I'll contact the hire company to see if the bike you want is available. I will then agree the dates, price and give you a few options. If you're happy, I'll put you in touch with a manager to make the deal."""
}


REPLIES = {
    'ru': {
        'welcome_message_reply': WELCOME_MESSAGE_TEXT['ru'],
        'initial_select_language': 'Выбери язык:',
        'main_menu_reply': 'Ты оказался в главном меню. Нажми “Арендовать байк” и я подберу для тебя актуальные предложения. ',
        'select_language_error': 'Выбери язык из списка',
        'rent_a_bike_init_reply': 'Заполни заявку на аренду',
        'rent_a_bike_reply': 'Какая модель тебя интересует?',
        'rent_a_bike_help_init_reply': HELP_MESSAGE_TEXT,
        'select_language': 'Выбери язык:',
        'select_main_menu_action': 'Выбери действие из списка',
        'prepare_bike_model_selected': 'Выбрана модель: {model.name}',
        'request_additional_params_reply': 'Хочешь указать дополнительные параметры байка?',
        'bike_model_selected': 'Выбрана модель: {model.name}',
        'back_client_menu_reply': 'Запрос отменен. Ты вернулся в главное меню.',
        'request_year_select': 'Хочешь ли ты ограничить год выпуска?',
        'request_helmets_select': 'Сколько шлемов тебе понадобится?',
        'requested_year_limit_label': 'Ограничение по году: {year_limit}',
        'request_color_select': 'Есть ли у тебя предпочтения по цвету?',
        'requested_color_limit_label': 'Предпочитаемый цвет: {color}',
        'request_abs_select': 'Нужен ли ABS?',
        'requested_abs_required_label': 'Нужен ABS',
        'requested_abs_not_required_label': 'ABS не нужен',
        'requested_abs_any_label': 'Наличие ABS неважно',
        'request_keyless_select': 'Нужен ли бесключевой доступ?',
        'requested_keyless_required_label': 'Нужен бесключевой доступ',
        'requested_keyless_not_required_label': 'Бесключевой доступ не нужен',
        'requested_keyless_any_label': 'Наличие бесключевого доступа неважно',
        'requested_one_helmet_required_label': 'Один шлем',
        'requested_two_helmets_required_label': 'Два шлема',
        'requested_no_helmets_label': 'Шлемы не нужны',
        'request_rent_start_select': 'Укажи когда ты хочешь начать аренду?',
        'rent_start_date_selected_reply': 'Дата начала аренды: {rent_start_date}',
        'request_rent_end_select': 'Укажи когда ты планируешь вернуть байк?',
        'rent_end_date_selected_reply': 'Дата конца аренды: {rent_end_date}',
        'rent_delivery_location_reply': 'Пришли, пожалуйста, локацию, куда нужно доставить байк',
        'rent_delivery_location_selected_reply': 'Координаты получены',
        'rent_confirmation_reply': ORDER_CONFIRMATION,
        'simple_rent_confirmation_reply': SIMPLE_ORDER_CONFIRMATION,
        'request_complete_ask_reply': 'Сейчас я опрашиваю сервисы аренды. Поиск продлится не более 5 минут.\nПо мере подтверждения предложения начнут появляться в чате.',
        'new_rental_request': 'Привет! Интересует “{bike.model.name}” на “{rent_amount}”!\nОн свободен сейчас?',
        'request_complete_nothing_found_reply': 'Нет подходящих байков. Попробуй изменить параметры поиска',
        'accepted_offer_reply': 'Отличный выбор. Менеджер свяжется с тобой в течении 5ти минут. Но если ты торопишься, нажми “Написать менеджеру”',
        'new_offer_for_manager': NEW_MANAGER_OFFER_REPLY,
        'active_request_chat_with_manager_select_action': 'Для разговора с менеджером нажми на кнопку',
        'active_request_state_select_action': 'Выбери действие из списка',
        'back_simple_client_menu_reply': 'Ты вернулся в главное меню'
    },
    'en': {
        'welcome_message_reply': WELCOME_MESSAGE_TEXT['en'],
        'initial_select_language': 'Select language:',
        'main_menu_reply': 'You are on the main menu. Click on "Rent a Bike" and I will show you the current offers. ',
        'select_language_error': 'Select language from list',
        'rent_a_bike_init_reply': 'Fill in the rental request form ',
        'rent_a_bike_reply': 'What model are you interested in? ',
        'rent_a_bike_help_init_reply': HELP_MESSAGE_TEXT_EN,
        'select_language': 'Select language:',
        'select_main_menu_action': 'Select action from list',
        'prepare_bike_model_selected': 'Selected model: {model.name}',
        'request_additional_params_reply': 'Do you want to specify additional bike parameters?',
        'bike_model_selected': 'Selected model: {model.name}',
        'back_client_menu_reply': 'Request canceled. Returned to main menu.',
        'request_year_select': 'Do you want to limit the year of manufacture?',
        'request_helmets_select': 'How many helmets do you need?',
        'requested_year_limit_label': 'Year limit: from {year_limit}',
        'request_color_select': 'Do you have a colour preference?',
        'requested_color_limit_label': 'Prefered colour: {color}',
        'request_abs_select': 'Do you need ABS?',
        'requested_abs_required_label': 'ABS needed',
        'requested_abs_not_required_label': 'ABS not needed',
        'requested_abs_any_label': 'Doesnt matter',
        'request_keyless_select': 'Do you need keyless entry?',
        'requested_keyless_required_label': 'Keyless entry needed',
        'requested_keyless_not_required_label': 'Keyless entry not needed',
        'requested_keyless_any_label': 'Doesnt matter',
        'requested_one_helmet_required_label': 'One helmet',
        'requested_two_helmets_required_label': 'Two helmets',
        'requested_no_helmets_label': 'No helmets',
        'request_rent_start_select': 'Indicate when you would like to start renting?',
        'rent_start_date_selected_reply': 'Rental start date: {rent_start_date}',
        'request_rent_end_select': 'When would you like to return the bike?',
        'rent_end_date_selected_reply': 'Rental end date: {rent_end_date}',
        'rent_delivery_location_reply': 'Please send me the location where you would like to deliver the bike',
        'rent_delivery_location_selected_reply': 'Received coordinates',
        'rent_confirmation_reply': ORDER_CONFIRMATION_EN,
        'simple_rent_confirmation_reply': SIMPLE_ORDER_CONFIRMATION_EN,
        'request_complete_ask_reply': 'I\'m currently searching for rental services. The search will take no more than 5 minutes.\nAs soon as it is confirmed, offers will appear in the chat.',
        'new_rental_request': 'Hi, I am interested in a "{bike.model.name}" for "{rent_amount}" days!\nIs it available now?',
        'request_complete_nothing_found_reply': 'Scooters not found. Try to change search criteria',
        'accepted_offer_reply': 'Great choice. A manager will get back to you within 5 minutes. But if you\'re in a hurry, click "Talk to a manager ".',
        'new_offer_for_manager': NEW_MANAGER_OFFER_REPLY,
        'active_request_chat_with_manager_select_action': 'Press button below to chat with manager',
        'active_request_state_select_action': 'Select language from list',
        'back_simple_client_menu_reply': 'Returned to main menu'
    },
    'id': {
        'welcome_message_reply': WELCOME_MESSAGE_TEXT['en'],
        'initial_select_language': 'Select language:',
        'main_menu_reply': 'You are on the main menu. Click on "Rent a Bike" and I will show you the current offers. ',
        'select_language_error': 'Select language from list',
        'rent_a_bike_init_reply': 'Fill in the rental request form ',
        'rent_a_bike_reply': 'What model are you interested in? ',
        'rent_a_bike_help_init_reply': HELP_MESSAGE_TEXT_EN,
        'select_language': 'Select language:',
        'select_main_menu_action': 'Select action from list',
        'prepare_bike_model_selected': 'Selected model: {model.name}',
        'request_additional_params_reply': 'Do you want to specify additional bike parameters?',
        'bike_model_selected': 'Selected model: {model.name}',
        'back_client_menu_reply': 'Request canceled. Returned to main menu.',
        'request_year_select': 'Do you want to limit the year of manufacture?',
        'request_helmets_select': 'How many helmets do you need?',
        'requested_year_limit_label': 'Year limit: from {year_limit}',
        'request_color_select': 'Do you have a colour preference?',
        'requested_color_limit_label': 'Prefered colour: {color}',
        'request_abs_select': 'Do you need ABS?',
        'requested_abs_required_label': 'ABS needed',
        'requested_abs_not_required_label': 'ABS not needed',
        'requested_abs_any_label': 'Doesnt matter',
        'request_keyless_select': 'Do you need keyless entry?',
        'requested_keyless_required_label': 'Keyless entry needed',
        'requested_keyless_not_required_label': 'Keyless entry not needed',
        'requested_keyless_any_label': 'Doesnt matter',
        'requested_one_helmet_required_label': 'One helmet',
        'requested_two_helmets_required_label': 'Two helmets',
        'requested_no_helmets_label': 'No helmets',
        'request_rent_start_select': 'Indicate when you would like to start renting?',
        'rent_start_date_selected_reply': 'Rental start date: {rent_start_date}',
        'request_rent_end_select': 'When would you like to return the bike?',
        'rent_end_date_selected_reply': 'Rental end date: {rent_end_date}',
        'rent_delivery_location_reply': 'Please send me the location where you would like to deliver the bike',
        'rent_delivery_location_selected_reply': 'Received coordinates',
        'rent_confirmation_reply': ORDER_CONFIRMATION_EN,
        'simple_rent_confirmation_reply': SIMPLE_ORDER_CONFIRMATION_EN,
        'request_complete_ask_reply': 'I\'m currently searching for rental services. The search will take no more than 5 minutes.\nAs soon as it is confirmed, offers will appear in the chat.',
        'request_complete_nothing_found_reply': 'Scooters not found. Try to change search criteria',
        'accepted_offer_reply': 'Great choice. A manager will get back to you within 5 minutes. But if you\'re in a hurry, click "Talk to a manager ".',
        'new_offer_for_manager': NEW_MANAGER_OFFER_REPLY,
        'active_request_chat_with_manager_select_action': 'Press button below to chat with manager',
        'active_request_state_select_action': 'Select language from list',
        'new_rental_request': 'Hi, saya tertarik dengan "{bike.model.name}" untuk "{rent_amount}"!\nApakah tersedia sekarang?',
    }
}

MANAGERS_UNAVAILABLE = {
    'ru': "Извините, в данный момент менеджеры недоступны.",
    'en': "Sorry, managers are not available at the moment.",
}

CONTACT_MANAGER = {
    'ru': "Вы можете связаться с менеджером, нажав на кнопку ниже:",
    'en': "You can contact the manager by pressing the button below:",
}

SUBSCRIBE_TO_CHANNEL = {
    'ru': "Пожалуйста, подпишитесь на наш канал, чтобы начать использовать бота. Затем вернитесь в бота и попробуйте снова.",
    'en': "Please subscribe to our channel to start using the bot. Then return to the bot and try again.",
}
