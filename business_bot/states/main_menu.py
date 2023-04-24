from aiogram.dispatcher.filters.state import State, StatesGroup


class MainMenuState(StatesGroup):
    garage_id = State()
    not_selected = State()
