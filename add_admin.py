from database.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Добавьте значения для first_name, last_name, language и telegram_id
new_admin = User(telegram_id=123456789, username="admin", email="admin@example.com", password=hash_password("12345"),
                 is_superuser=True,
                 is_active=True, first_name="Admin", last_name="User", language="en")
import config
from tortoise import Tortoise


async def add_admin():
    await Tortoise.init(config=config.TORTOISE_ORM)
    await new_admin.save()


import asyncio

asyncio.run(add_admin())
