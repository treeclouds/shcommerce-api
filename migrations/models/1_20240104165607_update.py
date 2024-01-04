from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "products" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "image" VARCHAR(255) NOT NULL,
    "category" VARCHAR(100) NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "condition" VARCHAR(14) NOT NULL,
    "price" DECIMAL(10,2) NOT NULL,
    "dimensions_width" DOUBLE PRECISION NOT NULL,
    "dimensions_height" DOUBLE PRECISION NOT NULL,
    "dimensions_length" DOUBLE PRECISION NOT NULL,
    "dimensions_weight" DOUBLE PRECISION NOT NULL,
    "brand" VARCHAR(100),
    "material" VARCHAR(100),
    "stock" INT NOT NULL,
    "sku" VARCHAR(100) NOT NULL,
    "tags" JSONB NOT NULL,
    "seller_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "products"."condition" IS 'brand_new: brand-new\nmint_condition: mint condition\nlike_new: like-new\nexcellent: excellent\ngood: good\nfair: fair';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "products";"""
