from datetime import datetime

from rq.decorators import job

import rq_worker as rh
import requests
import config


def post_kit(serial):
    r = requests.post("{base_url}/kit".format(base_url=config.api["base_url"]), json={"serial": serial})
    return r.json()


def get_kit(kit_id):
    r = requests.get("{base_url}/{id}/kit".format(base_url=config.api["base_url"], id=kit_id))
    return r.json()


@job('post', connection=rh.redis_server, timeout=5)
def post_value(base_url, api_kit_id, measurement_id, last_value, timestamp):
    requests.post("{base_url}/{kit_id}/{measurement_id}/values".format(base_url=base_url, kit_id=api_kit_id,
                                                                       measurement_id=measurement_id),
                  json={
                      "data": last_value,
                      "timestamp": datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
                  })


def post_sensor(kit_id, name, model):
    post_body = {"kit_id": kit_id, "name": name, "model": model}
    return requests.post("{}/{}/sensor".format(config.api["base_url"], kit_id), json=post_body).json()


def post_measurement(kit_id, sensor_id, symbol, name):
    post_body = {"sensor_id": sensor_id, 'symbol': symbol, 'name': name}
    r = requests.post("{}/{}/measurement".format(config.api["base_url"], kit_id), json=post_body).json()
    return r.json()
