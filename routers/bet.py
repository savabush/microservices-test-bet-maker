import logging

import aiohttp
from fastapi import APIRouter, HTTPException

from models.bet import Bet, BetList
from repositories.bet import BetRepository
from repositories.event_client import EventClient
from repositories.redis import EventRedisRepository
from services.redis import RedisCache

logger = logging.getLogger(__name__)

bet_router = APIRouter()


@bet_router.post(
    "/bet",
)
async def create_bet(
        bet: Bet,
) -> Bet:
    if await BetRepository.bet_exists(bet.id):
        raise HTTPException(status_code=409, detail="Bet already exists")
    
    if not await EventRedisRepository.event_exists(bet.event_id):
        async with aiohttp.ClientSession() as session:
            response = await EventClient.fetch_event(event_id=bet.event_id, session=session)
            logger.debug("Get new events")

            async with RedisCache().pipeline(transaction=True) as pipe:
                await EventRedisRepository.set_event(response, pipe=pipe)
                await pipe.execute()
                logger.debug("Cached new events")

    bet = await BetRepository.create_bet(bet)
    return bet


@bet_router.get("/bets")
async def get_all_bets() -> BetList:
    bets = await BetRepository.get_all_bets()
    return BetList(bets=bets)