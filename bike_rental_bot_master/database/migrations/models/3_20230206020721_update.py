from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bikeoffer" ADD "business_message_id" VARCHAR(255) NOT NULL  DEFAULT '';
        ALTER TABLE "bikeoffer" ADD "client_id" BIGINT NOT NULL;
        ALTER TABLE "bikeoffer" ADD "client_message_id" VARCHAR(255) NOT NULL  DEFAULT '';
        ALTER TABLE "bikeoffer" ALTER COLUMN "status" SET DEFAULT 0;
        ALTER TABLE "bikeoffer" ALTER COLUMN "status" TYPE SMALLINT USING "status"::SMALLINT;
        ALTER TABLE "bikeoffer" ADD CONSTRAINT "fk_bikeoffe_user_36153133" FOREIGN KEY ("client_id") REFERENCES "user" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bikeoffer" DROP CONSTRAINT "fk_bikeoffe_user_36153133";
        ALTER TABLE "bikeoffer" DROP COLUMN "business_message_id";
        ALTER TABLE "bikeoffer" DROP COLUMN "client_id";
        ALTER TABLE "bikeoffer" DROP COLUMN "client_message_id";
        ALTER TABLE "bikeoffer" ALTER COLUMN "status" DROP DEFAULT;
        ALTER TABLE "bikeoffer" ALTER COLUMN "status" TYPE SMALLINT USING "status"::SMALLINT;"""
