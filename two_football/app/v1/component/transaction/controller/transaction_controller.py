from flask import jsonify, Blueprint, request
from app.v1.generic.util.authorization_filter import pre_authorize
from app.v1.generic.util.validator import validate_payload
from app.v1.generic.constant.role_constant import ROLE_USER
from app.v1.generic.response.error_response import FORBIDDEN_RESPONSE, BAD_CARD_REQUEST, USER_NOT_FOUND
from app.v1.generic.response.status_code import *
from ..schema.card_schema import CardSchema
from app.v1.component.user.model.user import User
from app import bcrypt
from ..model.card import Card
import datetime

transaction = Blueprint('transaction', __name__)


@transaction.route('/users/<int:user_id>/balance', methods=['POST'])
@pre_authorize(ROLE_USER)
@validate_payload(CardSchema, BAD_CARD_REQUEST)
def deposit(user_id, token_id):
    if user_id != token_id:
        return jsonify(FORBIDDEN_RESPONSE), FORBIDDEN

    data = request.json

    user = User.find_user_by_id(user_id)
    if user is None:
        return jsonify(USER_NOT_FOUND), BAD_REQUEST

    # check password
    if bcrypt.check_password_hash(user.password, data.get('password')) is False:
        return jsonify(BAD_CARD_REQUEST), BAD_REQUEST

    card = Card.find_card_by_code(data.get('code'))
    if card is None or card.active is False:
        return jsonify(BAD_CARD_REQUEST), BAD_REQUEST

    previous_balance = user.balance
    card.load()
    user.deposit(card.value)

    return jsonify({
        'status': True,
        'bill': {
            'card_amount': card.value,
            'previous_balance': previous_balance,
            'balance': user.balance,
            'user_id': user_id,
            'deposit_time': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        }
    })
