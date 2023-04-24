import os
import aioredis as redis
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise
from backend.admin.providers import LoginProvider
from fastapi_admin.i18n import TRANSLATIONS, Translations
from fastapi_admin.app import app as admin_app
from database.models import User
from . import constants
import config


TRANSLATIONS['ru_RU'] = Translations.load(os.path.join(constants.BASE_DIR, 'locales'), locales='ru_RU')
print(TRANSLATIONS)

app = FastAPI()

app.mount(
    '/static',
    StaticFiles(directory='backend/static'),
    name='static'
)

templates = Jinja2Templates(directory='backend/templates')

register_tortoise(
    app,
    config=config.TORTOISE_ORM
)


@app.on_event('startup')
async def startup():
    await admin_app.configure(
        redis=redis.from_url(
            config.ADMIN_REDIS_URL,
            decode_responses=True,
            encoding='utf8'
        ),
        default_locale='ru_RU',
        template_folders=[os.path.join(constants.BASE_DIR, 'templates/admin')],
        language_switch=False,
        admin_path='/administrator',
        providers=[
            LoginProvider(
                admin_model=User
            )
        ]
    )


app.mount('/administrator', admin_app)

from .admin import routes
from .admin import resources