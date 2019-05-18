from flask import jsonify, Blueprint, request, render_template
from app.v1.generic.util.authorization_filter import pre_authorize
from app.v1.generic.constant.role_constant import ROLE_USER
from app.v1.generic.util.validator import validate_payload
from ..schema.comment_request_schema import CommentRequestSchema
from ..schema.comment_schema import CommentSchema
from app.v1.generic.response.error_response import BAD_COMMENT
from ..model.comment import Comment
from app.v1.generic.response.status_code import OK, BAD_REQUEST
from app.v1.component.fixture.model.match import Match
from app.v1.component.user.model.user import User
from app.v1.generic.response.error_response import MATCH_NOT_FOUND
from app.v1.generic.constant.pusher_constant import COMMENT_CHANNEL, COMMENT_EVENT_PREFIX
import threading
from app import pusher_client


comment_blueprint = Blueprint('comment_blueprint', __name__)


@comment_blueprint.route('/matches/<int:match_id>/comments', methods=['POST'])
@pre_authorize(ROLE_USER)
@validate_payload(CommentRequestSchema, BAD_COMMENT)
def post_comment(match_id, token_id):
    match = Match.find_match_by_id(match_id)

    if match is None:
        return jsonify(MATCH_NOT_FOUND), BAD_REQUEST

    comment_content = request.json
    comment = Comment(match_id, token_id, comment_content.get('comment'))

    async_task = threading.Thread(target=save_comment, kwargs={'comment': comment})
    async_task.start()

    return jsonify({
        'status': True,
        'data': {
            'match_id': match_id,
            'user_id': token_id,
            'time': comment.time.strftime('20%y-%m-%dT%H:%M:%S'),
            'comment': comment_content.get('comment')
        }
    }), OK


@comment_blueprint.route('/matches/<int:match_id>/comments', methods=['GET'])
def get_comments(match_id):
    match = Match.find_match_by_id(match_id)

    if match is None:
        return jsonify(MATCH_NOT_FOUND), BAD_REQUEST

    number = request.args.get('number')
    if number is None:
        number = 5

    schema = CommentSchema(many=True)
    comments = schema.dump(Comment.find_comments_of_match(match_id, number)).data

    return jsonify({
        'data': comments
    }), OK


# for test
@comment_blueprint.route('/matches', methods=['GET'])
def match_page():

    return render_template('match.html')


def save_comment(comment):
    from app import app
    with app.app_context():
        user = User.find_user_by_id(comment.user_id)
        data = {
            'user': {
                'user_id': user.user_id,
                'name': user.name
            },
            'comment': comment.comment,
            'match_id': comment.match_id
        }
        event = COMMENT_EVENT_PREFIX + str(comment.match_id)
        pusher_client.trigger(COMMENT_CHANNEL, event, data)

        comment.save()