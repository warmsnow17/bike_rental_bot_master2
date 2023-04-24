from urllib.parse import urlparse
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.executor import Executor
from database import db
from .middleware import UserMiddleware, ReplyMiddleware, OptionMiddleware
import config

bot = Bot(token=config.BUSINESS_BOT_TOKEN, parse_mode=types.ParseMode.HTML, timeout=5)

redis_url = urlparse(config.BUSINESS_BOT_REDIS_URL)
storage = RedisStorage2(host=redis_url.hostname, port=redis_url.port, password=redis_url.password, db=0)

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(OptionMiddleware())
dp.middleware.setup(UserMiddleware())
dp.middleware.setup(ReplyMiddleware())

from . import handlers

executor = Executor(dp, skip_updates=True)


@executor.on_startup
async def init(dispatcher: Dispatcher):
    await db.init(config=config.TORTOISE_ORM)


@executor.on_shutdown
async def shutdown(dispatcher: Dispatcher):
    await db.close_connections()
