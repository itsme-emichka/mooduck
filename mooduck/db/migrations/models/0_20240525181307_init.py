from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(128) NOT NULL UNIQUE,
    "password" VARCHAR(128) NOT NULL,
    "email" VARCHAR(512) NOT NULL UNIQUE,
    "name" VARCHAR(512)  UNIQUE,
    "role" VARCHAR(10) NOT NULL  DEFAULT 'user',
    "bio" TEXT
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
CREATE TABLE IF NOT EXISTS "item" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL,
    "description" TEXT,
    "item_type" VARCHAR(128) NOT NULL,
    "link" VARCHAR(1024),
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "author_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "itemmedia" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "media_type" VARCHAR(64) NOT NULL,
    "media_url" VARCHAR(512) NOT NULL,
    "item_id" BIGINT NOT NULL REFERENCES "item" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "moodboard" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(512) NOT NULL,
    "description" TEXT,
    "cover" VARCHAR(1024),
    "is_private" BOOL NOT NULL  DEFAULT False,
    "is_chaotic" BOOL NOT NULL  DEFAULT False,
    "author_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "favmoodboard" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "moodboard_id" BIGINT NOT NULL REFERENCES "moodboard" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "itemmoodboard" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "item_id" BIGINT NOT NULL REFERENCES "item" ("id") ON DELETE CASCADE,
    "moodboard_id" BIGINT NOT NULL REFERENCES "moodboard" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "comment" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "text" VARCHAR(2048) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "edited_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "answering_to_id" BIGINT REFERENCES "comment" ("id") ON DELETE CASCADE,
    "author_id" BIGINT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "moodboard_id" BIGINT NOT NULL REFERENCES "moodboard" ("id") ON DELETE CASCADE
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
