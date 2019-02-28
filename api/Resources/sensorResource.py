import falcon
from models import Kit, Value
from custom_helpers import validate
from sqlalchemy import exists

class SensorResource(object):


    @validate
    def on_put(self, req, resp, **kwargs):
        try:
            body = kwargs.get("parsed")
            serial = body['serial']

            kit = self.session.query(Kit).get(serial)
            value_list = kit.get_n_from_kit(self.session, serial, body.get("amount",0))
            resp.status = falcon.HTTP_201
            resp.medi = {'kit': kit.as_dict(), 'values': [value.as_dict for value in value_list]}

        except Exception:
            resp.status = falcon.HTTP_400
            resp.body = {'error': "Bad Request"}


    @validate
    def on_post(self, req, resp, **kwargs):
        try:
            body = kwargs.get("parsed")
            serial = body["serial"]
            #If kit already exists
            if not self.session.query(exists().where(Kit.serial==serial)).scalar(): 
                b = Kit(serial)
                b.save(self.session)
                resp.media = b.as_dict
            else: 
                resp.status = falcon.HTTP_403
                resp.media = {"error": "Box already exists"}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.body = {'error': "Bad Request"}
