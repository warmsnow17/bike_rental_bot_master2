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
    }
}

NEW_MANAGER_OFFER_REPLY = """
Подтверждение по заявке {offer.request.pk}
Клиент: @{offer.client.username}
Байк: {offer.bike.model.name} с номером {offer.bike.number}
Поставщик: @{offer.bike.user.username}
Срок аренды: {offer.request.rent_amount} дней
Цена: {offer.price} IDR
Стоимость: {offer.total_sum} IDR
Дата: {offer.request.created_at_date}
"""

ORDER_CONFIRMATION = """Остался последний шаг!
Проверь свой заказ и нажми на кнопку снизу

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
Проверь свой заказ и нажми на кнопку снизу

Модель скутера: {model_obj.name}
Сколько шлемов нужно: {helmets_label}
Вид аренды: {rent_type_label}
Дата начала аренды: {rent_start_date}
Дата возвращения байка: {rent_end_date}
Геопозиция: {lat} {lon}
"""

HELP_MESSAGE_TEXT = """
Если ты недавно освоил байк и нужна возможность ездить вдвоем – бери Yamaha NMax или Honda PCX. Это почти идентичные модели, главная разница в дизайне.

Honda Scoopy – отличный вариант, если ты хочешь найти самый недорогой скутер или если твой рост до 170см. Он самый компактный и легкий, на нем проще всего учиться.

Если хочешь недорогой, но немного больше и шустрее, чем Scoopy – бери Honda Vario или Yamaha Lexi, еще чуть больше чем Vario.

Если ты уже давно ездишь на скутерах (и на максискутерах тоже), и ты планируешь много длинных поездок, в том числе вдвоем – твой выбор Yamaha Xmax, один из самых больших скутеров в Индонезии.

Какую модель выбираешь?"""

WELCOME_MESSAGE_TEXT = {
    'ru': """Привет! Я бот "{full_name}". Помогу тебе найти скутер на Бали за 5 минут по выгодной цене""",
    'en': """Hi there!"""
}
