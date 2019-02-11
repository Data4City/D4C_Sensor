import falcon
from models import Kit
from custom_helpers import validate


class KitResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        b = Kit(serial= 10132)
        self.session.add(b)
        self.session.commit()
        resp.body = "naisu"

    @validate
    def on_post(self, req, resp, **kwargs):
        resp.body ="WAt"