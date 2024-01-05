from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "products" ADD "images" JSONB NOT NULL;
        ALTER TABLE "products" DROP COLUMN "image";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "products" ADD "image" VARCHAR(255) NOT NULL;
        ALTER TABLE "products" DROP COLUMN "images";"""
