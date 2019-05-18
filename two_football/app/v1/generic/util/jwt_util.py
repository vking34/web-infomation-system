from app.v1.config.security_config import JWT_SECRET_KEY
import jwt
import datetime


class JwtUtil:

    @staticmethod
    def generate_token(user_id, role, username):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=4),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id,
                'role': role,
                'username': username
            }
            return jwt.encode(
                payload,
                JWT_SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e
