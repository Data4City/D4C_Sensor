import json
import falcon
import jsonschema

def validate(func, schema = None):
        def wrapper(self, req, resp, *args, **kwargs):
            try:
                data = req.stream.read(req.content_length or 0)
                if len(data) == 0:
                    obj = ""
                else:
                    obj = json.loads(data.decode('utf-8'))
            except Exception:
                raise falcon.HTTPBadRequest(
                    'Invalid data',
                    'Could not properly parse the provided data as JSON'
                )

            if(schema is not None and obj != ""):
                try:
                    jsonschema.validate(obj, schema)
                except jsonschema.ValidationError as e:
                    raise falcon.HTTPBadRequest(
                        'Failed data validation',
                        e.message
                    )
            return func(self, req, resp, *args, parsed=obj, **kwargs)
        return wrapper