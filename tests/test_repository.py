import pytest

from models.bet import Bet
from tests.fixtures.fixtures import *


@pytest.mark.asyncio
async def test_create_bet(in_memory_db, bet_repository):
    bet = Bet(id=1, event_id=1, sum=100)
    created_bet = await bet_repository.create_bet(bet)
    assert created_bet.id is not None
    assert created_bet.event_id == bet.event_id
    assert created_bet.sum == bet.sum


@pytest.mark.asyncio
async def test_get_all_bets(in_memory_db, bet_repository):
    bet1 = Bet(id=2, event_id=1, sum=100)
    bet2 = Bet(id=3, event_id=2, sum=200)
    await bet_repository.create_bet(bet1)
    await bet_repository.create_bet(bet2)
    bets = await bet_repository.get_all_bets()
    assert len(bets) == 3