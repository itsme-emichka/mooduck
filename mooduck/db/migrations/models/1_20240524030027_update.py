from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ALTER COLUMN "name" DROP NOT NULL;
        CREATE UNIQUE INDEX "uid_user_email_1b4f1c" ON "user" ("email");
        CREATE UNIQUE INDEX "uid_user_name_76f409" ON "user" ("name");
        CREATE UNIQUE INDEX "uid_user_usernam_9987ab" ON "user" ("username");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_user_usernam_9987ab";
        DROP INDEX "idx_user_name_76f409";
        DROP INDEX "idx_user_email_1b4f1c";
        ALTER TABLE "user" ALTER COLUMN "name" SET NOT NULL;"""
