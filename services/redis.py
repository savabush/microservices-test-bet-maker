import asyncio
import logging
import sys

from redis import exceptions
from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

from config.settings import settings
from services.utils import singleton

logger = logging.getLogger(__name__)


@singleton
class RedisCache(Redis):
    def __init__(self):
        super().__init__(
            connection_pool=ConnectionPool(
                host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
            ),
            max_connections=settings.REDIS_MAX_CONNECTIONS,
        )


@singleton
class RedisHealthChecker(Redis):
    def __init__(self):
        self.heath_checker = None
        super().__init__(
            connection_pool=ConnectionPool(
                host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
            ),
            max_connections=settings.REDIS_MAX_CONNECTIONS,
        )

    async def init(self):
        self.heath_checker = asyncio.create_task(self._health_check())
        logger.info("запущен Redis health check")

    async def _health_check(self):
        while True:
            await asyncio.sleep(2)
            try:
                if not await self.ping():
                    logger.critical("Произошел разрыв соединения с базой данных Redis ")
                    sys.exit(1)
            except (Exception, exceptions.ConnectionError) as e:
                logger.critical(f"Произошел разрыв соединения с базой данных Redis {e}")
                sys.exit(1)
