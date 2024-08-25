import json
import logging

from models.event import UpdateEventState
from models.outbox import OutboxState
from repositories.bet import BetRepository
from services.consumer import KafkaConsumer
from services.producer import KafkaProducer
from services.utils import singleton

logger = logging.getLogger(__name__)


@singleton
class OutboxBetService(BetRepository):

    async def process_messages(self):
        logger.info("Start handling event service")
        async with KafkaConsumer(topics=['event']) as consumer:
            async for message in consumer.get_messages():
                logger.info("Receive event: %s", message)
                try:
                    await self._handle_message(message)
                except Exception as e:
                    logger.error(e, exc_info=True)
                    await self._handle_error(message)

    async def _handle_message(self, message: str):
        event = UpdateEventState.parse_raw(message)
        await self.update_bet_states(event_id=event.event_id, state=event.state)
        logger.info("Success handle event: %s", event)
        await self._produce_outbox(outbox_id=event.outbox_id, state=OutboxState.ACCESS)

    async def _produce_outbox(self, outbox_id: int, state: OutboxState):

        logger.info(f"Send event to Kafka: {outbox_id} - {state}")
        await KafkaProducer().send('outbox', json.dumps(
            {
                "outbox_id": outbox_id,
                "state": state.value,
             }
        ))
            
    async def _handle_error(self, message: str):
        event = UpdateEventState.parse_raw(message)
        await self._produce_outbox(outbox_id=event.outbox_id, state=OutboxState.ERROR)
        logger.error(f"Send error event to Kafka: {event.outbox_id} - {OutboxState.ERROR}")
