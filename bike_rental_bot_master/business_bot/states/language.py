from aiogram.dispatcher.filters.state import State, StatesGroup


class SelectLanguageState(StatesGroup):
    initial_setup = State()
    language = State()
