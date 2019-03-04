import falcon

from Helpers.custom_decorators import validate, get_json_body
from Helpers.helper_functions import get_or_create
from models import Kit, Sensor


class SensorResource(object):

    @validate
    @get_json_body
    def on_put(self, req, resp, **kwargs):
        try:
            body = kwargs.get("parsed")
            serial = body['serial']
            sensor_id = body['']
            kit = self.session.query(Kit).get(serial)
            value_list = kit.get_n_from_kit(self.session, serial, body.get("amount",0))
            resp.status = falcon.HTTP_201
            resp.medi = {'kit': kit.as_dict(), 'values': [value.as_dict for value in value_list]}

        except Exception:
            resp.status = falcon.HTTP_400
            resp.body = {'error': "Bad Request"}


    @get_json_body
    @validate
    def on_post(self, req, resp, **kwargs):
        try:
            body = kwargs.get("parsed")
            sensor = get_or_create(self.session, Sensor, name= body["name"], model=body["model"])
            kit = get_or_create(self.session, Kit, id=body["kit_id"])
            sensor.add_kit(kit, self.session)
            resp.media = sensor.as_dict
            resp.status = falcon.HTTP_201
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.body = {'error': "Bad Request"}
