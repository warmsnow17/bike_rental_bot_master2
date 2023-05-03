from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bikeoffer" ALTER COLUMN "status" TYPE SMALLINT USING "status"::SMALLINT;
        ALTER TABLE "rentalrequest" ADD "manager_id" BIGINT;
        ALTER TABLE "rentalrequest" ADD "status" SMALLINT NOT NULL  DEFAULT 0;
        ALTER TABLE "rentalrequest" ADD CONSTRAINT "fk_rentalre_user_198e9e29" FOREIGN KEY ("manager_id") REFERENCES "user" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "rentalrequest" DROP CONSTRAINT "fk_rentalre_user_198e9e29";
        ALTER TABLE "bikeoffer" ALTER COLUMN "status" TYPE SMALLINT USING "status"::SMALLINT;
        ALTER TABLE "rentalrequest" DROP COLUMN "manager_id";
        ALTER TABLE "rentalrequest" DROP COLUMN "status";"""
