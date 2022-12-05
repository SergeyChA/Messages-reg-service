import aio_pika
import asyncio
import time
from fastapi import FastAPI

from . import models
from .database import engine, database, metadata


app = FastAPI()

metadata.create_all(engine)


async def save_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process():
        message = message.body.decode('utf-8')
        query = models.messages.insert().values(**eval(message))
        await database.connect()
        await database.execute(query)
        await database.disconnect()
        # Delay message to view in RabbitMQ
        await asyncio.sleep(20)


@app.on_event("startup")
async def startup() -> None:
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq/")
    queue_name = 'queue'
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name, auto_delete=False)
    await queue.consume(save_message)

    try:
        await asyncio.Future()
    finally:
        await connection.close()
