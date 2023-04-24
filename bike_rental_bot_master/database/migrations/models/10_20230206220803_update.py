from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "rentalrequest" ADD "lat" DOUBLE PRECISION NOT NULL  DEFAULT 0;
        ALTER TABLE "rentalrequest" ADD "helmets" VARCHAR(255) NOT NULL  DEFAULT '';
        ALTER TABLE "rentalrequest" ADD "lon" DOUBLE PRECISION NOT NULL  DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "rentalrequest" DROP COLUMN "lat";
        ALTER TABLE "rentalrequest" DROP COLUMN "helmets";
        ALTER TABLE "rentalrequest" DROP COLUMN "lon";"""
