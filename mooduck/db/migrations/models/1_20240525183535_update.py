from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "chaotic_id" BIGINT;
        ALTER TABLE "user" ADD CONSTRAINT "fk_user_moodboar_0fe26358" FOREIGN KEY ("chaotic_id") REFERENCES "moodboard" ("id") ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP CONSTRAINT "fk_user_moodboar_0fe26358";
        ALTER TABLE "user" DROP COLUMN "chaotic_id";"""
