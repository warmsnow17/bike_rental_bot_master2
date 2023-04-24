from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "option" ALTER COLUMN "value" TYPE VARCHAR(255) USING "value"::VARCHAR(255);
        ALTER TABLE "option" ALTER COLUMN "value" TYPE VARCHAR(255) USING "value"::VARCHAR(255);
        ALTER TABLE "option" ALTER COLUMN "value" TYPE VARCHAR(255) USING "value"::VARCHAR(255);
        ALTER TABLE "option" ALTER COLUMN "option_type" SET DEFAULT '';
        ALTER TABLE "option" ALTER COLUMN "option_type" TYPE VARCHAR(100) USING "option_type"::VARCHAR(100);
        ALTER TABLE "option" ALTER COLUMN "option_type" TYPE VARCHAR(100) USING "option_type"::VARCHAR(100);
        ALTER TABLE "option" ALTER COLUMN "option_type" TYPE VARCHAR(100) USING "option_type"::VARCHAR(100);
        ALTER TABLE "option" ALTER COLUMN "key" TYPE VARCHAR(255) USING "key"::VARCHAR(255);
        ALTER TABLE "option" ALTER COLUMN "key" TYPE VARCHAR(255) USING "key"::VARCHAR(255);
        ALTER TABLE "option" ALTER COLUMN "key" TYPE VARCHAR(255) USING "key"::VARCHAR(255);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "option" ALTER COLUMN "value" TYPE TEXT USING "value"::TEXT;
        ALTER TABLE "option" ALTER COLUMN "value" TYPE TEXT USING "value"::TEXT;
        ALTER TABLE "option" ALTER COLUMN "value" TYPE TEXT USING "value"::TEXT;
        ALTER TABLE "option" ALTER COLUMN "option_type" TYPE TEXT USING "option_type"::TEXT;
        ALTER TABLE "option" ALTER COLUMN "option_type" DROP DEFAULT;
        ALTER TABLE "option" ALTER COLUMN "option_type" TYPE TEXT USING "option_type"::TEXT;
        ALTER TABLE "option" ALTER COLUMN "option_type" TYPE TEXT USING "option_type"::TEXT;
        ALTER TABLE "option" ALTER COLUMN "key" TYPE TEXT USING "key"::TEXT;
        ALTER TABLE "option" ALTER COLUMN "key" TYPE TEXT USING "key"::TEXT;
        ALTER TABLE "option" ALTER COLUMN "key" TYPE TEXT USING "key"::TEXT;"""
