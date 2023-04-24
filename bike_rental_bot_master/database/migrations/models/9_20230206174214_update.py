from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bikebooking" ADD "offer_id" INT NOT NULL;
        ALTER TABLE "bikebooking" ADD CONSTRAINT "fk_bikebook_bikeoffe_44225da4" FOREIGN KEY ("offer_id") REFERENCES "bikeoffer" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "bikebooking" DROP CONSTRAINT "fk_bikebook_bikeoffe_44225da4";
        ALTER TABLE "bikebooking" DROP COLUMN "offer_id";"""
