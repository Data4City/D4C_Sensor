import asyncio
from redis import Redis
from rq import Queue, Connection, Worker

redis_server = Redis()
q = Queue(connection=redis_server)

def process_workers(queues: list = ['post']):
    print("adup")
    try:
        with Connection():
            w = Worker(queues)
            w.work()
    except Exception as e: 
        print("nigger")
        print(e)
        print(type(e))

