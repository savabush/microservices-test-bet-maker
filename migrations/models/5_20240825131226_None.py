from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "betmodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "event_id" INT NOT NULL,
    "sum" DECIMAL(8,2) NOT NULL,
    "status" VARCHAR(12) NOT NULL  DEFAULT 'NOT_FINISHED'
);
COMMENT ON COLUMN "betmodel"."id" IS 'ID';
COMMENT ON COLUMN "betmodel"."event_id" IS 'ID события';
COMMENT ON COLUMN "betmodel"."sum" IS 'Сумма';
COMMENT ON COLUMN "betmodel"."status" IS 'Статус';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
