from aiogram.dispatcher.filters.state import State, StatesGroup


class CalendarState(StatesGroup):
    calendar = State()
    rent_bikes = State()
    available_bikes = State()
