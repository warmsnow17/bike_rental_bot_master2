from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "rentalrequest" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "additional_params" BOOL NOT NULL,
    "year_from" INT NOT NULL,
    "mileage_to" INT NOT NULL,
    "color" VARCHAR(255) NOT NULL,
    "abs" VARCHAR(255) NOT NULL,
    "keyless" VARCHAR(255) NOT NULL,
    "rent_type" VARCHAR(255) NOT NULL,
    "rent_amount" INT NOT NULL,
    "rent_start_date" TIMESTAMPTZ NOT NULL,
    "model_id" INT NOT NULL REFERENCES "bikemodel" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);;
        ALTER TABLE "user" ADD "is_business" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "user" ADD "is_client" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "user" ADD "is_manager" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "user" ADD "is_admin" BOOL NOT NULL  DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "is_business";
        ALTER TABLE "user" DROP COLUMN "is_client";
        ALTER TABLE "user" DROP COLUMN "is_manager";
        ALTER TABLE "user" DROP COLUMN "is_admin";
        DROP TABLE IF EXISTS "rentalrequest";"""
