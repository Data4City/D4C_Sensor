import json
import falcon
import jsonschema


def validate(func, schema=None):
    def wrapper(self, req, resp, *args, **kwargs):
        try:
            obj = kwargs.get('parsed', req.stream.read(req.content_length or 0))
        except Exception as e:
            raise falcon.HTTPBadRequest(
                'Failed data validation, no valid body',
                e.message
            )
        if schema is not None and obj != "":
            try:
                jsonschema.validate(obj, schema)
            except jsonschema.ValidationError as e:
                raise falcon.HTTPBadRequest(
                    'Failed data validation',
                    e.message
                )
        return func(self, req, resp, *args, **kwargs)

    return wrapper


def get_json_body(func):
    def wrapper(self, req, resp, *args, **kwargs):
        try:
            data = req.stream.read(req.content_length or 0)
            if len(data) == 0:
                obj = ""
            else:
                obj = json.loads(data.decode('utf-8'))
        except Exception:
            raise falcon.HTTPBadRequest(
                'Invalid data', 'Could not properly parse the provided data as JSON')
        return func(self, req, resp, *args, parsed=obj, **kwargs)

    return wrapper


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance