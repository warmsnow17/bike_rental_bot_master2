from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bikeoffer" ADD "price_with_fee" DECIMAL(8,2) NOT NULL  DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bikeoffer" DROP COLUMN "price_with_fee";"""
