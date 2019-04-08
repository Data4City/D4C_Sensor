from rq.decorators import job

from Helpers import redis_helper as rh


class RequestsHandler:

    @job('post', connection=rh.redis_server, timeout=5)
    def post_sensor(self, data: dict, user_id, socket_emit: bool = False):
        #TODO Change path
        route = data.pop("type")
        print(data)
        #requests.post("http://localhost/api/{}:8888", data)

        #if socket_emit:
        #    fh.publish_message("update", data)


