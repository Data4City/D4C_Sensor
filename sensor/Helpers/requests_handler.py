from rq.decorators import job

from sensor.Helpers import rq_worker as rh
import requests
from sensor import config

kit_id = None


def post_kit(serial):
    r = requests.post("{}/kit".format(config.api["base_url"]), json={"serial": serial})
    resp = r.json()
    global kit_id
    if "id" in resp and not kit_id:
        kit_id = resp["id"]
    return resp


def get_kit(serial):
    r = requests.get("{}/kit".format(config.api["base_url"]), json={"serial": serial}).json()
    global kit_id

    if "id" in r and not kit_id:
        kit_id = r["id"]
    return r


@job('post', connection=rh.redis_server, timeout=5)
def post_value(data: dict):
    print("Posting?")
    route = data.pop("type")
    requests.post("{}/{}/{}".format(config.api["base_url"], kit_id, route), json=data)


def post_sensor(sensor_info):
    post_body = {"kit_id": kit_id, "name": sensor_info["name"], "model": sensor_info["model"]}
    return requests.post("{}/{}/sensor".format(config.api["base_url"], kit_id), json=post_body).json()


def post_measurement(sensor_id, measurement_info):
    post_body = {"sensor_id": sensor_id, 'symbol': measurement_info['symbol'], 'name': measurement_info['name']}
    return requests.post("{}/{}/measurement".format(config.api["base_url"], kit_id), json=post_body).json()
