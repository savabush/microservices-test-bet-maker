import logging

from models.bet import Bet, BetReturn, BetState
from models.event import EventState
from schemas import BetModel


logger = logging.getLogger(__name__)


class BetRepository:

    @classmethod
    async def create_bet(cls, bet: Bet) -> Bet:
        instance = await BetModel.create(**bet.dict())
        logger.debug(f"Bet created  by {cls.__name__}: {instance}")
        bet_db = Bet.from_orm(instance)
        return bet_db
    
    @classmethod
    async def get_bet(cls, bet_id: int) -> Bet:
        instance = await BetModel.get(id=bet_id)
        event_db = Bet.from_orm(instance)
        return event_db
    
    @classmethod
    async def bet_exists(cls, bet_id: int) -> bool:
        return await BetModel.exists(id=bet_id)
    
    @classmethod
    async def __get_bet_for_update(cls, event_id: int) -> BetModel:
        instance = await BetModel.select_for_update().get(id=event_id)
        return instance
    
    @classmethod
    async def update_bet_states(cls, event_id: int, state: EventState) -> BetState:
        states = {
            EventState.NEW: BetState.NOT_FINISHED,
            EventState.FINISHED_WIN: BetState.WIN,
            EventState.FINISHED_LOSE: BetState.LOSE
        }
        new_state = states.get(state)
        await BetModel.select_for_update().filter(event_id=event_id).update(status=new_state)
        return new_state
    
    @classmethod
    async def get_all_bets(cls) -> list[BetReturn]:
        instances = await BetModel.all()
        events_db = [BetReturn.from_orm(instance) for instance in instances]
        return events_db