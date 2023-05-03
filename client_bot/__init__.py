from urllib.parse import urlparse
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.executor import Executor
from database import db
from .middleware import UserMiddleware, ReplyMiddleware, OptionMiddleware
import config

bot = Bot(token=config.CLIENT_BOT_TOKEN, parse_mode=types.ParseMode.HTML, timeout=5)

redis_url = urlparse(config.CLIENT_BOT_REDIS_URL)
storage = RedisStorage2(host=redis_url.hostname, port=redis_url.port, password=redis_url.password, db=1)

dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(OptionMiddleware())
dp.middleware.setup(UserMiddleware())
dp.middleware.setup(ReplyMiddleware())

from . import handlers

executor = Executor(dp, skip_updates=True)


async def on_startup(dp):
    # await bot.send_message(chat_id=config.ADMIN_ID, text="Бот запущен")

    await bot.set_my_commands(
        [
            types.BotCommand(command="restart_bot", description="Перезапустить бота"),
            types.BotCommand(command="contact_manager", description="Написать менеджеру"),
        ]
    )
    await db.init(config=config.TORTOISE_ORM)

async def on_shutdown(dp):
    await db.close_connections()

@executor.on_startup
async def init(dispatcher: Dispatcher):
    await on_startup(dispatcher)

@executor.on_shutdown
async def shutdown(dispatcher: Dispatcher):
    await on_shutdown(dispatcher)
