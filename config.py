import os

<<<<<<< HEAD

DEBUG = os.getenv('DEBUG', '0') == '1'
BUSINESS_BOT_TOKEN = os.getenv('BUSINESS_BOT_TOKEN')
CLIENT_BOT_TOKEN = os.getenv('CLIENT_BOT_TOKEN')
=======
DEBUG = os.getenv('DEBUG', '0') == '1'
BUSINESS_BOT_TOKEN = os.getenv('BUSINESS_BOT_TOKEN', '')
CLIENT_BOT_TOKEN = os.getenv('CLIENT_BOT_TOKEN', '')
>>>>>>> dev

BACKEND_HOST = os.getenv('BACKEND_HOST', '127.0.0.1')
BACKEND_PORT = int(os.getenv('BACKEND_PORT', 8000))
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000')

BUSINESS_BOT_REDIS_URL = os.getenv('BUSINESS_BOT_REDIS_URL', 'redis://localhost:6379/bikes_business')
CLIENT_BOT_REDIS_URL = os.getenv('CLIENT_BOT_REDIS_URL', 'redis://localhost:6379/bikes_client')
ADMIN_REDIS_URL = os.getenv('ADMIN_REDIS_URL', 'redis://localhost:6379/2')

TORTOISE_ORM = {
    'connections': {'default': os.getenv('DATABASE_URL', 'postgres://postgres:postgres@localhost:5432/bikes')},
    'apps': {
        'models': {
            'models': ['database.models', 'aerich.models'],
            'default_connection': 'default',
        },
    },
}

DEFAULT_LANGUAGE = 'en'

BUSINESS_BOT_LANGUAGES = [
    {
        'code': 'en',
        'name': '🇺🇸 Английский',
        'native_name': '🇺🇸 English'
    },
    {
        'code': 'id',
        'name': '🇮🇩 Индонизийский',
        'native_name': '🇮🇩 Bahasa Indonesia'
    }
]

CLIENT_BOT_LANGUAGES = [
    {
        'code': 'ru',
        'name': '🇷🇺 Русский',
        'native_name': '🇷🇺 Русский'
    },
    {
        'code': 'en',
        'name': '🇺🇸 Английский',
        'native_name': '🇺🇸 English'
    }
]
