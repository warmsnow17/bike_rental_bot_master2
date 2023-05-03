from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bike" ADD "threeweekly_price" DECIMAL(10,2) NOT NULL  DEFAULT 0;
        ALTER TABLE "bike" ADD "biweekly_price" DECIMAL(10,2) NOT NULL  DEFAULT 0;
        ALTER TABLE "bike" ADD "bimonthly_price" DECIMAL(10,2) NOT NULL  DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bike" DROP COLUMN "threeweekly_price";
        ALTER TABLE "bike" DROP COLUMN "biweekly_price";
        ALTER TABLE "bike" DROP COLUMN "bimonthly_price";"""
