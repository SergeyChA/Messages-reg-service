import aio_pika
import asyncio
import json
from fastapi import FastAPI

from . import schemas
from . import models
from .database import engine, metadata


app = FastAPI()


async def save_message(message: schemas.SaveMessage):
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
        await conn.execute(models.messages.insert(), message)
        await engine.dispose()


async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process():
        message_decode = message.body.decode('utf-8')
        message_to_dict = json.loads(message_decode)
        await save_message(message_to_dict)
        # Delay message to view in RabbitMQ
        await asyncio.sleep(20)


@app.on_event("startup")
async def startup() -> None:
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    queue_name = 'queue'
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name, auto_delete=False)
    await queue.consume(process_message)

    try:
        await asyncio.Future()
    finally:
        await connection.close()
