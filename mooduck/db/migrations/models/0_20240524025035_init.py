from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(128) NOT NULL,
    "password" VARCHAR(128) NOT NULL,
    "email" VARCHAR(512) NOT NULL,
    "name" VARCHAR(512) NOT NULL,
    "role" VARCHAR(10) NOT NULL  DEFAULT 'user'
);
CREATE TABLE IF NOT EXISTS "notebook" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "notebook" TEXT NOT NULL,
    "owner_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "subscription" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "subscribed_for_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "subscriber_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
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
