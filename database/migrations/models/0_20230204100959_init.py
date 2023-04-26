from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "bikemodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "option" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "key" TEXT NOT NULL,
    "option_type" TEXT NOT NULL,
    "value" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "replymessage" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "action" TEXT NOT NULL,
    "language" TEXT NOT NULL,
    "message" TEXT NOT NULL,
    CONSTRAINT "uid_replymessag_action_b8182f" UNIQUE ("action", "language")
);
CREATE TABLE IF NOT EXISTS "user" (
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "telegram_id" BIGINT NOT NULL UNIQUE,
    "username" VARCHAR(255) NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "language" VARCHAR(3) NOT NULL,
    "active" BOOL NOT NULL  DEFAULT True,
    "role" SMALLINT NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_user_usernam_9987ab" ON "user" ("username");
COMMENT ON COLUMN "user"."role" IS 'CLIENT: 1\nBUSINESS: 2\nMANAGER: 3\nADMINISTRATOR: 4';
CREATE TABLE IF NOT EXISTS "bike" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "year" INT NOT NULL,
    "mileage" INT NOT NULL,
    "color" VARCHAR(255) NOT NULL,
    "abs" BOOL NOT NULL,
    "keyless" BOOL NOT NULL,
    "number" VARCHAR(100) NOT NULL,
    "price" DECIMAL(10,2) NOT NULL,
    "rental_start_date" TIMESTAMPTZ,
    "model_id" INT NOT NULL REFERENCES "bikemodel" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "bikebooking" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "from_date" TIMESTAMPTZ NOT NULL,
    "to_date" TIMESTAMPTZ NOT NULL,
    "bike_id" INT NOT NULL REFERENCES "bike" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "bikephoto" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "telegram_id" VARCHAR(255) NOT NULL,
    "file" VARCHAR(255) NOT NULL  DEFAULT '',
    "bike_id" INT NOT NULL REFERENCES "bike" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "garage" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" TEXT NOT NULL,
    "owner_name" TEXT NOT NULL,
    "lat" DOUBLE PRECISION NOT NULL,
    "lon" DOUBLE PRECISION NOT NULL,
    "owner_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
