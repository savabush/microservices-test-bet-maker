import json
import logging

import aiohttp
from fastapi import APIRouter

from models.event import Event
from repositories.event_client import EventClient
from repositories.redis import EventRedisRepository
from services.redis import RedisCache


logger = logging.getLogger(__name__)
event_router = APIRouter()


@event_router.get("/events")
async def get_events_from_line_provider() -> list[Event]:
    if events := await EventRedisRepository.get_events():
        logger.debug("Events get from cache")
        return list(map(lambda x: Event(**json.loads(x)), events.values()))
    
    async with aiohttp.ClientSession() as session:
        response = await EventClient.fetch_events(session=session)
        logger.debug("Get new events")

        async with RedisCache().pipeline(transaction=True) as pipe:
            await EventRedisRepository.set_events(response, pipe=pipe)
            await pipe.execute()
            logger.debug("Cached new events")

        return list(map(lambda x: Event(**x), response))
