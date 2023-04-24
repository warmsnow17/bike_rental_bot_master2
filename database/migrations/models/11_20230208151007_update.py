from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "password" VARCHAR(255) NOT NULL  DEFAULT '';
        DROP TABLE IF EXISTS "usertoken";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "password";"""
