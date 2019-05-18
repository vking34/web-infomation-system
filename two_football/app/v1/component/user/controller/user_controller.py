from flask import jsonify, Blueprint, request
from ..model.user import User
from ..schema.user_schema import UserSchema, UpdatingProfileSchema
from app.v1.generic.util.authorization_filter import pre_authorize
from app.v1.generic.constant.role_constant import ROLE_USER, ROLE_ADMIN
from app.v1.generic.util.validator import validate_payload
from app.v1.generic.response.error_response import BAD_UPDATING_PROFILE_FORM, INVALID_TOKEN, \
    USER_NOT_FOUND, EMAIL_TAKEN, PHONE_TAKEN
from app.v1.generic.response.status_code import *
import threading


users_blueprint = Blueprint('users_blueprint', __name__)


@users_blueprint.route('/users', methods=['GET'])
@pre_authorize(ROLE_ADMIN)
def get_users():
    schema = UserSchema(many=True)
    return jsonify({'students': schema.dump(User.find_users()).data})


@users_blueprint.route('/users/<int:user_id>', methods=['PUT'])
@pre_authorize(ROLE_USER)
@validate_payload(UpdatingProfileSchema, BAD_UPDATING_PROFILE_FORM)
def update_profile(user_id, token_id):
    user = User.find_user_by_id(user_id)
    if user is None:
        return jsonify(USER_NOT_FOUND), BAD_REQUEST
    if user_id != token_id:
        return jsonify(INVALID_TOKEN), FORBIDDEN

    profile = request.json
    name = profile.get('name')
    email = profile.get('email')
    phone = profile.get('phone')

    user_record = User.find_user_by_email_or_phone(email, phone)
    if user_record is not None and user_record.user_id != user_id:
        print(user.email)
        print(user.phone)
        print(user_record.email)
        print(user_record.phone)
        if user_record.email == email:
            return jsonify(EMAIL_TAKEN), BAD_REQUEST
        return jsonify(PHONE_TAKEN), BAD_REQUEST

    async_task = threading.Thread(target=save_profile, kwargs={'user': user, 'name': name, 'email': email, 'phone': phone})
    async_task.start()

    return jsonify({
        'status': True,
        'user': {
            'user_id': user.user_id,
            'role': user.role,
            'username': user.username,
            'name': name,
            'email': email,
            'phone': phone,
            'balance': user.balance
        }
    })


def save_profile(user, name, email, phone):
    from app import app
    with app.app_context():
        user.update_profile(name, email, phone)
