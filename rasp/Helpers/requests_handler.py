import requests
from Helpers import plugged_sensor
from Helpers import flask_helper as fh
from Helpers import redis_helper as rh

from rq.decorators import job

@job('post', connection=rh.redis_server, timeout=5)
def post_sensor(data: dict, socket_emit: bool = False):
    #TODO Change path
    print(data)
    requests.post("http://localhost:8888", data)
    if socket_emit:
        fh.publish_message("update", data)