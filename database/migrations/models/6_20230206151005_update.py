from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bikeoffer" ADD "price" DECIMAL(8,2) NOT NULL  DEFAULT 0;
        ALTER TABLE "bikeoffer" ADD "total_sum" DECIMAL(8,2) NOT NULL  DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bikeoffer" DROP COLUMN "price";
        ALTER TABLE "bikeoffer" DROP COLUMN "total_sum";"""
