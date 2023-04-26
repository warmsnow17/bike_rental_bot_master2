from aiogram.dispatcher.filters.state import State, StatesGroup


class SelectLanguageState(StatesGroup):
    language = State()
