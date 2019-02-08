import falcon
from models import Box
class BoxResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        b = Box(serial= 10132)
        self.session.add(b)
        resp.body = b
