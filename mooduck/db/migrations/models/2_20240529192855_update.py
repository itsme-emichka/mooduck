from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" DROP COLUMN "edited_at";
        CREATE TABLE IF NOT EXISTS "like" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "author_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "moodboard_id" BIGINT NOT NULL REFERENCES "moodboard" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "comment" ADD "edited_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        DROP TABLE IF EXISTS "like";"""
