from aiogram.dispatcher.filters.state import State, StatesGroup


class MainMenuState(StatesGroup):
    not_selected = State()
