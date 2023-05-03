from aiogram.dispatcher.filters.state import State, StatesGroup


class RentRequestState(StatesGroup):
    prepare = State()
    model = State()
    additional_params = State()
    year = State()
    mileage = State()
    color = State()
    abs = State()
    keyless = State()
    helmets = State()
    rent_type = State()
    rent_amount = State()
    rent_start_date = State()
    rent_end_date = State()
    location = State()
    lat = State()
    lon = State()
    request_confirmation = State()
    help = State()
    choose = State()


class ActiveRequestState(StatesGroup):
    request_id = State()
