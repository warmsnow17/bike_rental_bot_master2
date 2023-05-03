from aiogram.dispatcher.filters.state import State, StatesGroup


class SetupGarageState(StatesGroup):
    owner_name = State()
    name = State()
    location = State()


class GarageState(StatesGroup):
    bikes_list = State()
    list_type = State()
    bike_details = State()
