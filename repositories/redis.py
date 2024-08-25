import json
import logging

from config.settings import settings
from services.redis import RedisCache
from redis.asyncio.client import Pipeline


logger = logging.getLogger(__name__)


class EventRedisRepository:
    
    @classmethod
    async def event_exists(cls, event_id: int) -> bool:
        return await RedisCache().exists(str(event_id))

    @classmethod
    async def get_events(cls) -> dict:
        return await RedisCache().hgetall("events")
    
    @classmethod
    async def set_events(cls, events: list[dict], pipe: Pipeline | None = None):
        pipe_created = False
        
        if pipe is None:
            pipe = RedisCache().pipeline(transaction=True)
            pipe_created = True

        for event in events:
            await pipe.hset("events", str(event["id"]), json.dumps(event))
        await pipe.expire("events", settings.REDIS_TTL)

        if pipe_created:
            logger.debug(f"Events cached by {cls.__name__}: {[event['id'] for event in events]}")
            await pipe.execute()
            await pipe.close()

    @classmethod
    async def set_event(cls, event: dict, pipe: Pipeline | None = None):
        pipe_created = False
        
        if pipe is None:
            pipe = RedisCache().pipeline(transaction=True)
            pipe_created = True

        await pipe.hset("events", str(event["id"]), json.dumps(event))
        await pipe.expire("events", settings.REDIS_TTL)

        if pipe_created:
            logger.debug(f"Event cached by {cls.__name__}: {event['id']} - {event}")
            await pipe.execute()
            await pipe.close()