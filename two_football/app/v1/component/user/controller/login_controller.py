from flask import jsonify, Blueprint, request, render_template
from ..schema.authen_form import AuthenticationForm
from ..schema.user_schema import UserSchema
from ..model.user import User
from app import bcrypt
from app.v1.generic.response.error_response import FAIL_LOGIN
from app.v1.generic.response.status_code import *
from app.v1.generic.util.jwt_util import JwtUtil

login_blueprint = Blueprint('login_blueprint', __name__)


@login_blueprint.route('/login', methods=['POST'])
def login():

    global result
    request_login = request.json
    schema = AuthenticationForm()

    result = schema.load(request_login)

    if len(result.errors) != 0:
        return jsonify({
            'status': False,
            'errors': result.errors
        })

    user = User.find_user_by_username(request_login.get('username'))
    if user is None:
        return jsonify(FAIL_LOGIN), BAD_REQUEST

    if bcrypt.check_password_hash(user.password, request_login.get('password')) is False:
        return jsonify(FAIL_LOGIN), BAD_REQUEST

    token_object = JwtUtil.generate_token(user.user_id, user.role, user.username)
    schema = UserSchema()
    return jsonify({
        'status': True,
        'access_token': token_object.decode(),
        'user': schema.dump(user).data
    })


@login_blueprint.route('/login', methods=['GET'])
def get_login_page():
    return render_template('login.html')

