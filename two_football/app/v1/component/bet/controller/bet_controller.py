from flask import jsonify, Blueprint, request
from app.v1.generic.util.authorization_filter import pre_authorize
from app.v1.generic.util.validator import validate_payload
from app.v1.generic.constant.role_constant import ROLE_USER
from app.v1.generic.response.error_response import BAD_BET_REQUEST, MATCH_NOT_FOUND, MATCH_FINISHED, \
    MATCH_LIVE, INVALID_BET_AMOUNT, BET_ALREADY, INVALID_TOKEN
from app.v1.generic.response.status_code import *
from app.v1.component.fixture.model.match import Match
from app.v1.component.user.model.user import User
from ..model.bet import Bet
from ..schema.bet_request_schema import BetRequestSchema
from ..schema.bet_schema import BetSchema
from ..schema.user_bet_schema import UserBetSchema
import datetime

bet_blueprint = Blueprint('bet_blueprint', __name__)


@bet_blueprint.route('/matches/<int:match_id>/bets', methods=['POST'])
@pre_authorize(ROLE_USER)
@validate_payload(BetRequestSchema, BAD_BET_REQUEST)
def bet_match(match_id, token_id):
    match = Match.find_match_by_id(match_id)

    if match is None:
        return jsonify(MATCH_NOT_FOUND), BAD_REQUEST

    if match.match_status == 'FT':
        return jsonify(MATCH_FINISHED), BAD_REQUEST

    if match.match_status != '':
        return jsonify(MATCH_LIVE), BAD_REQUEST

    user = User.find_user_by_id(token_id)
    bet_request = request.json

    if user.balance < bet_request.get('bet_amount'):
        return jsonify(INVALID_BET_AMOUNT), BAD_REQUEST

    bet_record = Bet.find_bet(user_id=token_id, match_id=match_id, bet_type=bet_request.get('bet_type'))
    if bet_record is not None:
        return jsonify(BET_ALREADY), BAD_REQUEST

    bet_time = datetime.datetime.now()
    bet_record = Bet(user_id=token_id,
                     match_id=match_id,
                     bet_type=bet_request.get('bet_type'),
                     bet_amount=bet_request.get('bet_amount'),
                     bet_content=bet_request.get('bet_content'),
                     bet_time=bet_time)

    bet_record.save()
    user.decrease_balance(bet_request.get('bet_amount'))

    return jsonify({
        'status': True,
        'bet': {
            'user_id': token_id,
            'match_id': match_id,
            'bet_type': bet_request.get('bet_type'),
            'bet_amount': bet_request.get('bet_amount'),
            'bet_content': bet_request.get('bet_content'),
            'bet_time': bet_time.strftime('20%y-%m-%dT%H:%M:%S'),
            'bet_status': 'PROCESSING'
        }
    }), OK


@bet_blueprint.route('/matches/<int:match_id>/bets', methods=['GET'])
@pre_authorize(ROLE_USER)
def get_user_bets_for_match(match_id, token_id):
    match = Match.find_match_by_id(match_id)

    if match is None:
        return jsonify(MATCH_NOT_FOUND), BAD_REQUEST

    schema = UserBetSchema(many=True)
    bets = schema.dump(Bet.find_user_bets_for_match(match_id, token_id)).data

    return jsonify({
        'status': True,
        'bets': bets
    }), OK


@bet_blueprint.route('/users/<int:user_id>/bets', methods=['GET'])
@pre_authorize(ROLE_USER)
def get_bets(user_id, token_id):
    if user_id != token_id:
        return jsonify(INVALID_TOKEN), FORBIDDEN

    schema = BetSchema(many=True)
    bets = schema.dump(Bet.find_bets_of_user(user_id)).data

    return jsonify({
        'status': True,
        'bets': bets
    }), OK

