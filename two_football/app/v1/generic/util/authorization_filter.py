from functools import wraps
from flask import request, jsonify
import jwt
from app.v1.generic.constant.header_constant import *
from app.v1.generic.response.error_response import MISSING_AUTHORIZATION_FIELD, BAD_AUTHORIZATION, \
    FORBIDDEN_RESPONSE, EXPIRED_TOKEN, INVALID_TOKEN
from app.v1.generic.response.status_code import UNAUTHORIZED, FORBIDDEN
from app.v1.config.security_config import JWT_SECRET_KEY


def pre_authorize(role):
    def filter(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            authorization_header = request.headers.get(AUTHORIZATION)

            if authorization_header is None:
                return jsonify(MISSING_AUTHORIZATION_FIELD), UNAUTHORIZED

            value_parts = authorization_header.split(" ")
            prefix = value_parts[0]

            if prefix != AUTH_PREFIX:
                return jsonify(BAD_AUTHORIZATION), UNAUTHORIZED

            access_token = value_parts[1]

            try:
                token = jwt.decode(access_token, JWT_SECRET_KEY, algorithms=['HS256'])
                if token['role'] != role:
                    return jsonify(FORBIDDEN_RESPONSE), FORBIDDEN

            except jwt.ExpiredSignatureError:
                return jsonify(EXPIRED_TOKEN), UNAUTHORIZED

            except jwt.InvalidTokenError:
                return jsonify(INVALID_TOKEN), UNAUTHORIZED

            kwargs['token_id'] = token['sub']
            return f(*args, **kwargs)
        return wrapper
    return filter
