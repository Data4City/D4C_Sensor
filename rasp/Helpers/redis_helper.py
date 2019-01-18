from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler

redis_server = Redis()
scheduler = Scheduler(connection=redis_server)