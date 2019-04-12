from rq.decorators import job

from Helpers import rq_worker as rh
import requests
from observable import Observable

obs = Observable()


class RequestHandler:
    def __init__(self, config):
        self.base_url = config["url"]
        self.kit_id = None

    def post_kit(self, serial):
        r = requests.post("{}/kit".format(self.base_url), json={"serial": serial}).json()
        if "id" in r and not self.kit_id:
            self.kit_id = r["id"]
        return r

    def get_kit(self, serial):
        r = requests.get("{}/kit".format(self.base_url), json={"serial": serial}).json()
        if "id" in r and not self.kit_id:
            self.kit_id = r["id"]
        return r

    @job('post', connection=rh.redis_server, timeout=5)
    def post_value(self, data: dict, socket_emit: bool = False):
        route = data.pop("type")
        requests.post("{}/{}".format(self.base_url, route), json=data)

        # if socket_emit:
        #    fh.publish_message("update", data)

    @obs.on("post_value_to_server")
    def handle_post_value(self, data):
        self.post_value.delay(data)

    def post_sensor(self, sensor_info):
        post_body = {"kit_id": self.kit_id, "name": sensor_info["name"], "model": sensor_info["model"]}
        return requests.post("{}/sensor".format(self.base_url), json=post_body).json()

    def post_measurement(self, sensor_id, measurement_info):
        post_body = {"sensor_id": sensor_id, 'symbol': measurement_info['symbol'], 'name': measurement_info['name']}
        return requests.post("{}/measurement".format(self.base_url), json=post_body).json()
