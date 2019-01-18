import requests
import plugged_sensor

from redis_helper import redis_server
from rq.decorators import job

@job('post', connection=redis_server, timeout=5)
def post_sensor(data: dict):
    #TODO Change path
    requests.post("http://localhost:8888", data)