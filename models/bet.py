import decimal
import enum
from pydantic import BaseModel
from pydantic import field_validator


class BetState(enum.Enum):
    NOT_FINISHED = "NOT_FINISHED"
    WIN = "WIN"
    LOSE = "LOSE"


class Bet(BaseModel):
    id: int
    event_id: int
    sum: decimal.Decimal
    status: BetState = BetState.NOT_FINISHED

    @field_validator('sum')
    @classmethod
    def check_sum(cls, v):
        if v.as_tuple().exponent < -2:
            raise ValueError('The sum field must have two digits after the point')
        if len(v.as_tuple().digits) + v.as_tuple().exponent > 6:
            raise ValueError('The sum field must have less or equal than 8 digits before the point')
        return v
    
    class Config:
        from_attributes = True


class BetReturn(BaseModel):
    event_id: int
    id: int
    status: BetState
    
    class Config:
        from_attributes = True


class BetList(BaseModel):
    bets: list[BetReturn]
