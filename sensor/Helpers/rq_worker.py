from rq import Connection, Worker
import logging
from redis import Redis
from rq import Queue

redis_server = Redis()
q = Queue(connection=redis_server)


def process_workers(queues):
    logger = logging.getLogger(__name__)
    try:
        with Connection():
            w = Worker(queues)
            w.work()
    except Exception as e:
        logger.error(str(e))



if __name__ == "__main__":
    process_workers()