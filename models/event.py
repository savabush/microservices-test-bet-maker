import datetime
import decimal
import enum
from pydantic import BaseModel


class EventState(enum.Enum):
    NEW = "NEW"
    FINISHED_WIN = "FINISHED_WIN"
    FINISHED_LOSE = "FINISHED_LOSE"


class Event(BaseModel):
    id: int
    coefficient: decimal.Decimal
    deadline: datetime.datetime
    state: EventState
    
    class Config:
        from_attributes = True
        

class UpdateEventState(BaseModel):
    outbox_id: int
    event_id: int
    state: EventState
