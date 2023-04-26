import asyncio
from aiogram import exceptions


async def send_message(bot, telegram_user_id, message, reply_markup):
    try:
        return await bot.send_message(telegram_user_id, message, reply_markup=reply_markup)
    except exceptions.RetryAfter as e:
        print(e)
        asyncio.sleep(e.timeout + 1)
        return await send_message(bot, telegram_user_id, message, reply_markup=reply_markup)
    except Exception as e:
        print(e)
        return False
