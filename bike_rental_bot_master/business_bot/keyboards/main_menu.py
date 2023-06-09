from aiogram import types
from business_bot import helpers



class MainMenuKeyboard:

    rows = [
        ['add_bike_button_label'],
        ['my_garage_button_label'],
        ['rental_calendar_button_label']
    ]

    def __init__(self, language: str) -> None:
        self.language = language

    @classmethod
    def get_button_id_by_text(cls, language: str, text: str) -> str:
        for row in cls.rows:
            button_id = row[0]
            button_text = helpers.language.get_translation(language, button_id, '')
            if button_text == text:
                return button_id
        return None

    def markup(self):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for row in self.rows:
            buttons = []
            for button_id in row:
                text = helpers.language.get_translation(self.language, button_id, button_id)
                buttons.append(types.KeyboardButton(text))
            keyboard.row(*buttons)
        return keyboard
