import falcon
from models import Kit, Value
from custom_helpers import validate


class KitResource(object):
    @validate
    def on_get(self, req, resp):
        try:
            body = kwargs.get("parsed")
            serial = body['serial']
            kit = self.session.query(Kit).get(serial)
            value_list = kit.get_n_from_kit(self.session, serial, body.get("amount",0))
            response = {'kit': kit.as_dict(), 'values': [value.as_dict() for value in value_list]}
            resp.status = falcon.HTTP_201
            resp.body = response

        except Exception:
            resp.status = falcon.HTTP_400
            resp.body = {'error': "Bad Request"}


    @validate
    def on_post(self, req, resp, **kwargs):
        try:
            print("nigga")
            print(kwargs)
            body = kwargs.get("parsed")
            b = Kit(body['serial'])
            b.save(self.session)
        except Exception as e:
            print(e)
            resp.status = falcon.HTTP_400
            resp.body = {'error': "Bad Request"}