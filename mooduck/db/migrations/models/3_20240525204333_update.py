from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "item" ADD "media" TEXT;
        ALTER TABLE "moodboard" ADD "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        DROP TABLE IF EXISTS "itemmedia";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "item" DROP COLUMN "media";
        ALTER TABLE "moodboard" DROP COLUMN "created_at";"""
