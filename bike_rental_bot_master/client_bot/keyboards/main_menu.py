from aiogram import types
from client_bot import helpers



class MainMenuKeyboard:

    rows = [
        ['rent_a_bike_button_label'],
        ['model_help_button_label'],
        ['select_language_button_label'],
    ]

    def __init__(self, language: str) -> None:
        self.language = language

    @classmethod
    def get_button_id_by_text(cls, language: str, text: str) -> str:
        for row in cls.rows:
            print(row, 'its row --------------------------')
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
