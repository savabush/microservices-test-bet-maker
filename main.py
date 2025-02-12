import asyncio
import logging.config

import uvicorn
from fastapi import FastAPI

from config.db import TortoiseDB
from config.logging import LOGGING_CONFIG
from repositories.outbox import OutboxBetService
from routers.bet import bet_router
from routers.event import event_router
from services.db import DBHealthChecker
from services.producer import KafkaProducer

from services.redis import RedisHealthChecker


logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(event_router)
app.include_router(bet_router)


@app.get('/health')
async def health_check():
    return 1


async def main():
    await RedisHealthChecker().init()
    await TortoiseDB().connect()
    await DBHealthChecker().init()
    await KafkaProducer().start()
    await OutboxBetService().process_messages()


if __name__ == "__main__":
    logger.info("Start bet-maker service")

    config = uvicorn.Config(app, host="0.0.0.0", port=8090, log_config=LOGGING_CONFIG)
    server = uvicorn.Server(config)

    loop = asyncio.get_event_loop()
    loop.create_task(server.serve())
    loop.create_task(main())

    loop.run_forever()
