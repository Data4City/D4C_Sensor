import falcon
from models import Kit, Value, Sensor, Measurement
from custom_helpers import validate, get_json_body
from sqlalchemy import exists

class KitResource(object):    
    
    @get_json_body
    def on_get(self, req, resp,**kwargs):
        try:
            body = kwargs.get("parsed")
            id = body.get("id")
            kit = self.session.query(Kit).get(1)
            if kit is not None:
               value_list = kit.get_values_from_kit(self.session, body.get("amount",[]))
               response = {}#{'kit': kit.as_dict, 'values': [value.as_dict for value in value_list]}
               resp.status = falcon.HTTP_201
               resp.media = response
            else:
               resp.status = falcon.HTTP_404
               resp.media = { 'error': "Box with id {} doesn't exist".format(id)}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.body = {'error': "Bad Request"}


    @get_json_body
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
        except falcon.HTTPBadRequest:
            resp.status = falcon.HTTP_400
            resp.body = {'error': "Bad Request"}
        except Exception as e: 
            print(e)