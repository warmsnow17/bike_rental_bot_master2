from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- Добавьте столбец garage_id с разрешением значений NULL
        ALTER TABLE "bike" ADD "garage_id" INT;

        -- Установите значение garage_id для существующих записей (пример: garage_id = 1)
        UPDATE "bike" SET "garage_id" = 1 WHERE "garage_id" IS NULL;

        -- Измените столбец garage_id на NOT NULL
        ALTER TABLE "bike" ALTER COLUMN "garage_id" SET NOT NULL;

        -- Добавьте ограничение FOREIGN KEY
        ALTER TABLE "bike" ADD CONSTRAINT "fk_bike_garage_063d4079" FOREIGN KEY ("garage_id") REFERENCES "garage" ("id") ON DELETE CASCADE;
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bike" DROP CONSTRAINT "fk_bike_garage_063d4079";
        ALTER TABLE "bike" DROP COLUMN "garage_id";"""
