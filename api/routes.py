import falcon
from falcon import API
from Resources import *


def get_app() -> API:
    _app = falcon.API()
    _app.add_route('/box', BoxResource())
    return _app