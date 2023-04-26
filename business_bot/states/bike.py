from aiogram.dispatcher.filters.state import State, StatesGroup


class BikeState(StatesGroup):
    list_type = State()
    bike_id = State()
    model = State()
    model_name = State()
    year = State()
    mileage = State()
    color = State()
    manual_color = State()
    abs = State()
    abs_label = State()
    keyless = State()
    keyless_label = State()
    number = State()
    price = State()
    weekly_price = State()
    biweekly_price = State()
    monthly_price = State()
    photos = State()
    review = State()
    availability_date = State()
