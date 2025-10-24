import asyncio
import logging

import aio_pika
import pandas as pd

RABBITMQ_URL = "amqp://guest:guest@localhost/"

logging.basicConfig(level=logging.INFO)

async def process_file(file_path):
    logging.info(f"Processing file: {file_path}")
    try:
        df = pd.read_csv(file_path)

        logging.info(f"File contents:\n{df.head()}")



        logging.info("Processing completed.")
    except Exception as e:
        logging.error(f"Failed processing {file_path}: {e}")

async def main():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("marks_queue", durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    file_path = message.body.decode()
                    await process_file(file_path)

if __name__ == "__main__":
    asyncio.run(main())
