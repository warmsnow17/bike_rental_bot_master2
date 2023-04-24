

TRANSLATIONS = {
    'ru': {
        'add_bike_button_label': 'Добавить байк',
        'my_garage_button_label': 'Мой гараж',
        'rental_calendar_button_label': 'Календарь аренды',
        'cancel_button_label': 'Отмена',
        'back_button_label': 'Назад',
        'yes_button_label': 'Да',
        'no_button_label': 'Нет',
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
        'other_color_label': 'Другой',
    },
    'en': {
        'add_bike_button_label': 'Add bike',
        'my_garage_button_label': 'My Garage',
        'rental_calendar_button_label': 'Rental Calendar',
        'cancel_button_label': 'Cancel',
        'back_button_label': 'Back',
        'yes_button_label': 'Yes',
        'no_button_label': 'No',
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
        'other_color_label': 'Other',
    },
    'id': {
        'add_bike_button_label': 'Add bike',
        'my_garage_button_label': 'My Garage',
        'rental_calendar_button_label': 'Rental Calendar',
        'cancel_button_label': 'Cancel',
        'back_button_label': 'Back',
        'yes_button_label': 'Yes',
        'no_button_label': 'No',
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
        'other_color_label': 'Other',
    }
}

DEFAULT_REVIEW_MESSAGE = """Проверь, все ли верно?

Модель: {model_name}
Год: {year}
Пробег: {mileage}
Цвет: {color_name}
ABS: {abs_label}
Keyless: {keyless_label}
Гос. номер: {number}
Цена за сутки: {price} IDR
Цена за неделю: {weekly_price} IDR
Цена за две недели: {biweekly_price} IDR
Цена за три недели: {threeweekly_price} IDR
Цена за месяц: {monthly_price} IDR
Цена за два месяца и более: {bimonthly_price} IDR"""

DEFAULT_BIKE_DETAILS_MESSAGE = """Здесь ты можешь изменить информацию о своем байке.
Модель: {bike.model.name}
Год: {bike.year}
Пробег: {bike.mileage}
Цвет: {color}
ABS: {abs_support}
Keyless: {keyless_support}
Гос. номер: {bike.number}
Цена за сутки: {bike.price} IDR
Цена за неделю: {bike.weekly_price} IDR
Цена за две недели: {bike.biweekly_price} IDR
Цена за три недели: {bike.threeweekly_price} IDR
Цена за месяц: {bike.monthly_price} IDR
Цена за два месяца и более: {bike.bimonthly_price} IDR"""

DEFAULT_BIKE_OFFER_MESSAGE = """Модель: {bike.model.name}
Год: {bike.year}
Пробег: {bike.mileage}
Цвет: {color}
ABS: {abs_support}
Keyless: {keyless_support}
Цена за сутки: {usd_price}K IDR
Стоимость: {usd_total_sum}K IDR"""


AGREEMENT = '''Прочитайте и примите условия пользователя.
Если вы согласны с условиями нажмите "Принять".\n\n"Условия использования
Бота.\n1. Клиент заплатит вам напрямую, бот может сопровождать проведение
сделки.\n2. Если вы не отвечаете на заявку в течении 24 часов, ваш объект
скрывается из каталога и больше не показывается клиентам.\n3. Сервис не
раскрывает информацию о своих пользователях."'''

WELCOME_MESSAGE = {
    'ru': """Привет! Я бот "{full_name}" и я умею находить новых клиентов.
Я задам тебе несколько вопросов, чтобы узнать о твоих байках и покажу их своим клиентам.
Далее я открою для тебя виртуальный офис, в котором ты сможешь контролировать бизнес. """,
    'en': """Привет! Я бот "{full_name}" и я умею находить новых клиентов.
Я задам тебе несколько вопросов, чтобы узнать о твоих байках и покажу их своим клиентам.
Далее я открою для тебя виртуальный офис, в котором ты сможешь контролировать бизнес. """,
    'id': """Привет! Я бот "{full_name}" и я умею находить новых клиентов.
Я задам тебе несколько вопросов, чтобы узнать о твоих байках и покажу их своим клиентам.
Далее я открою для тебя виртуальный офис, в котором ты сможешь контролировать бизнес. """
}