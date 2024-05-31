from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "moodboard" ADD "likes" INT NOT NULL  DEFAULT 0;
        ALTER TABLE "like" DROP COLUMN "created_at";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "like" ADD "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "moodboard" DROP COLUMN "likes";"""
