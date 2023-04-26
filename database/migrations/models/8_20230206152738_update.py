from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bikeoffer" ADD "total_sum_with_fee" DECIMAL(10,2) NOT NULL  DEFAULT 0;
        ALTER TABLE "bikeoffer" ALTER COLUMN "price" TYPE DECIMAL(10,2) USING "price"::DECIMAL(10,2);
        ALTER TABLE "bikeoffer" ALTER COLUMN "price_with_fee" TYPE DECIMAL(10,2) USING "price_with_fee"::DECIMAL(10,2);
        ALTER TABLE "bikeoffer" ALTER COLUMN "total_sum" TYPE DECIMAL(10,2) USING "total_sum"::DECIMAL(10,2);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bikeoffer" DROP COLUMN "total_sum_with_fee";
        ALTER TABLE "bikeoffer" ALTER COLUMN "price" TYPE DECIMAL(8,2) USING "price"::DECIMAL(8,2);
        ALTER TABLE "bikeoffer" ALTER COLUMN "price_with_fee" TYPE DECIMAL(8,2) USING "price_with_fee"::DECIMAL(8,2);
        ALTER TABLE "bikeoffer" ALTER COLUMN "total_sum" TYPE DECIMAL(8,2) USING "total_sum"::DECIMAL(8,2);"""
