from business_bot import constants
import config


def get_translation(language: str, identifier: str, default: str = '') -> str:
    return constants.TRANSLATIONS.get(language, config.DEFAULT_LANGUAGE).get(identifier, default)
