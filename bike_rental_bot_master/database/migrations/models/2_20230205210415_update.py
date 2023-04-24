from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bike" ADD "monthly_price" DECIMAL(10,2) NOT NULL  DEFAULT 0;
        ALTER TABLE "bike" ADD "weekly_price" DECIMAL(10,2) NOT NULL  DEFAULT 0;
        CREATE TABLE IF NOT EXISTS "bikeoffer" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "status" SMALLINT NOT NULL,
    "bike_id" INT NOT NULL REFERENCES "bike" ("id") ON DELETE CASCADE,
    "request_id" INT NOT NULL REFERENCES "rentalrequest" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "bikeoffer"."status" IS 'NEW: 0\nACCEPTED: 1\nREJECTED: 2';;
        ALTER TABLE "rentalrequest" ADD "rent_end_date" TIMESTAMPTZ;
        ALTER TABLE "rentalrequest" ADD "selected_offer_id" INT;
        ALTER TABLE "rentalrequest" ADD CONSTRAINT "fk_rentalre_bikeoffe_8799c820" FOREIGN KEY ("selected_offer_id") REFERENCES "bikeoffer" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "rentalrequest" DROP CONSTRAINT "fk_rentalre_bikeoffe_8799c820";
        ALTER TABLE "bike" DROP COLUMN "monthly_price";
        ALTER TABLE "bike" DROP COLUMN "weekly_price";
        ALTER TABLE "rentalrequest" DROP COLUMN "rent_end_date";
        ALTER TABLE "rentalrequest" DROP COLUMN "selected_offer_id";
        DROP TABLE IF EXISTS "bikeoffer";"""
