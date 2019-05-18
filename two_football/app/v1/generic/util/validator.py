from functools import wraps
from flask import request, jsonify
from marshmallow import ValidationError
from app.v1.generic.response.status_code import BAD_REQUEST


def validate_payload(filtering_schema, error_response):
    def filter(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            global result
            data = request.json

            schema = filtering_schema()
            try:
                result = schema.load(data)
            except ValidationError as error:
                print(error)

            if len(result.errors) != 0:
                return jsonify(error_response), BAD_REQUEST

            return f(*args, **kwargs)
        return wrapper
    return filter
