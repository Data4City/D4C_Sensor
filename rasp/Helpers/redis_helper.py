import asyncio
from redis import Redis
from rq import Queue, Connection, Worker

redis_server = Redis()
q = Queue(connection=redis_server)

async def process_workers(queues: list = ['post']):
    while True:
        try:
            with Connection():
                w = Worker(queues)
                w.work()
        except Exception as e: 
            print(e)
        
        asyncio.wait(20)
