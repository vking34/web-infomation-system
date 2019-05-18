from flask import jsonify, Blueprint, request, Response
from ..schema.register_form import RegisterFormSchema
from marshmallow import ValidationError
from ..model.user import User
from ..schema.user_schema import UserSchema
from app.v1.generic.response.error_response import SIGNUP_EXISTING_USER_ERROR
from app.v1.generic.response.status_code import *
signup_blueprint = Blueprint('signup_blueprint', __name__)


@signup_blueprint.route('/signup', methods=['POST'])
def sign_up():
    global result
    request_user = request.json
    schema = RegisterFormSchema()
    try:
        result = schema.load(request_user)
    except ValidationError as error:
        print(error)

    if len(result.errors) != 0:
        return jsonify(
            {
                'status': False,
                'errors': result.errors
            }
        )

    user_record = User.find_existing_user(request_user.get('username'),
                                          request_user.get('phone'),
                                          request_user.get('email'))
    if user_record is not None:
        return jsonify(SIGNUP_EXISTING_USER_ERROR), BAD_REQUEST

    user_record = User(request_user.get('username'),
                       request_user.get('password'),
                       request_user.get('name'),
                       request_user.get('phone'),
                       request_user.get('email'))
    user_record.save()

    schema = UserSchema()
    data = schema.dump(User.find_user_by_username(request_user.get('username'))).data

    return jsonify({
        'status': True,
        'user': data
    }), 200




