from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.v1.config.database_config import *
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import threading
import atexit
import pusher
# from apscheduler.schedulers.background import BackgroundScheduler
from app.v1.config.thread_config import POOL_TIME, fetch3rdAPI
from app.v1.generic.constant.pusher_constant import BET_CHANNEL, BET_EVENT_PREFIX


db = SQLAlchemy()
bcrypt = Bcrypt()

fetchingThread = threading.Thread()

pusher_client = pusher.Pusher(
  app_id='776278',
  key='831b0d6aebed3c727f01',
  secret='de6374931b709dbd3106',
  cluster='ap1',
  ssl=True
)

app = None

def create_app():
    global app
    app = Flask(__name__, template_folder='../templates')

    # db config
    db_uri = 'mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}'\
                .format(user=DB_USERNAME, pwd=DB_PASSWORD, host=DB_HOST, port=DB_PORT, db=DB_NAME)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # enable CORS
    CORS(app)

    # register blueprints
    from app.v1.component.user.controller.user_controller import users_blueprint
    from app.v1.component.user.controller.signup_controller import signup_blueprint
    from app.v1.component.user.controller.login_controller import login_blueprint
    from app.v1.component.transaction.controller.transaction_controller import transaction
    from app.v1.component.bet.controller.bet_controller import bet_blueprint
    from app.v1.component.comment.controller.comment_controller import comment_blueprint

    app.register_blueprint(signup_blueprint)
    app.register_blueprint(login_blueprint)
    app.register_blueprint(users_blueprint, url_prefix='/api/v1')
    app.register_blueprint(bet_blueprint, url_prefix='/api/v1')
    app.register_blueprint(transaction, url_prefix='/api/v1')
    app.register_blueprint(comment_blueprint, url_prefix='/api/v1')

    # add background thread
    def fetch():
        global fetchingThread

        # print(fetchingThread.getName())
        fetchingThread = threading.Timer(POOL_TIME, fetch)
        fetchingThread.start()

        # with app_context to use SQLalchemy
        with app.app_context():
            from app.v1.component.league.model.league import League

            league_list = League.find_leagues()

            for league in league_list:
                # print(league.league_id)
                # print(type(league.league_id))
                match_list = fetch3rdAPI(league.league_id)

                if match_list is None:
                    continue

                # print(match_list)
                from app.v1.component.fixture.model.match import Match

                for match in match_list:

                    match_id = int(match.get('match_id'))

                    # print('--------------------------------------')
                    # print(match_id)

                    league_id = int(match.get('league_id'))
                    if match.get('match_status') == '':
                        hometeam_halftime_score = 0
                        awayteam_halftime_score = 0
                        hometeam_score = 0
                        awayteam_score = 0
                        yellow_card = 0
                    else:
                        hometeam_halftime_score = int(match.get('match_hometeam_halftime_score'))
                        awayteam_halftime_score = int(match.get('match_awayteam_halftime_score'))

                        if match.get('match_hometeam_score') == '':
                            hometeam_score = 0
                        else:
                            hometeam_score = int(match.get('match_hometeam_score'))

                        if match.get('match_awayteam_score') == '':
                            awayteam_score = 0
                        else:
                            awayteam_score = int(match.get('match_awayteam_score'))

                        statistics = match.get('statistics')
                        full_time = False
                        for statistic in statistics:
                            if statistic.get('type') == 'yellow cards':
                                yellow_card = int(statistic.get('home')) + int(statistic.get('away'))
                                full_time = True
                                break
                        if full_time is False:
                            yellow_card = 0

                    # print('match_hometeam_score: ' + str(hometeam_score))
                    # print('match_hometeam_halftime_score: ' + str(hometeam_halftime_score))
                    # print('yellow card: ' + str(yellow_card))

                    match_record = Match.find_match_by_id(match_id)
                    if match_record is None:
                        # print('insert ' + str(match_id))
                        match_record = Match(match_id=match_id,
                                             league_id=league_id,
                                             match_date=match.get('match_date'),
                                             match_time=match.get('match_time'),
                                             match_hometeam_name=match.get('match_hometeam_name'),
                                             match_awayteam_name=match.get('match_awayteam_name'),
                                             match_hometeam_halftime_score=hometeam_halftime_score,
                                             match_awayteam_halftime_score=awayteam_halftime_score,
                                             match_hometeam_score=hometeam_score,
                                             match_awayteam_score=awayteam_score,
                                             yellow_card=yellow_card,
                                             match_status=match.get('match_status')
                                             )
                        match_record.save()
                        continue

                    match_status_before = match_record.match_status
                    if match.get('match_status') != '' and match_record.match_status != 'FT':
                        # update match
                        print('update ' + str(match_id))
                        match_record.update(match_hometeam_halftime_score=hometeam_halftime_score,
                                            match_awayteam_halftime_score=awayteam_halftime_score,
                                            match_hometeam_score=hometeam_score,
                                            match_awayteam_score=awayteam_score,
                                            yellow_card=yellow_card,
                                            match_status=match.get('match_status'))

                    if match.get('match_status') == 'FT' and match_status_before != 'FT':
                        print('calculate ' + str(match_id))
                        # calculate bets ...
                        from app.v1.component.bet.model.bet import Bet
                        from app.v1.component.user.model.user import User

                        bet_list = Bet.find_bets_of_match(match_id)
                        for bet in bet_list:

                            # half time bet
                            if bet.bet_type == 1:
                                predict_result = bet.bet_content.split('-')
                                print('bet type: ' + str(bet.bet_type))
                                print(predict_result)
                                if int(predict_result[0]) == match_record.match_hometeam_halftime_score and int(predict_result[1]) == match_record.match_awayteam_halftime_score:
                                    user = User.find_user_by_id(bet.user_id)
                                    bet_gain = bet.bet_amount * 2
                                    user.deposit(bet_gain)
                                    bet.end(bet_gain)

                                else:
                                    bet.end(0)

                            # full time bet
                            if bet.bet_type == 2:
                                predict_result = bet.bet_content.split('-')
                                print('bet type: ' + str(bet.bet_type))
                                print(predict_result)
                                if int(predict_result[0]) == match_record.match_hometeam_score and int(predict_result[1]) == match_record.match_awayteam_score:
                                    user = User.find_user_by_id(bet.user_id)
                                    bet_gain = bet.bet_amount * 3
                                    user.deposit(bet_gain)
                                    bet.end(bet_gain)
                                else:
                                    bet.end(0)

                            # yellow card bet
                            if bet.bet_type == 3:
                                print('bet type: ' + str(bet.bet_type))
                                print(bet.bet_content)
                                if int(bet.bet_content) == match_record.yellow_card:
                                    user = User.find_user_by_id(bet.user_id)
                                    bet_gain = bet.bet_amount * 2
                                    user.deposit(bet_gain)
                                    bet.end(bet_gain)
                                else:
                                    bet.end(0)

                            # pusher
                            event = BET_EVENT_PREFIX + str(match_id) + '_' + str(bet.user_id)
                            print(event)
                            from app.v1.component.fixture.schema.match_schema import MatchSchema
                            schema = MatchSchema()
                            data = {
                                'match': schema.dump(match_record).data,
                                'bet_type': bet.bet_type,
                                'bet_amount': bet.bet_amount,
                                'bet_content': bet.bet_content,
                                'bet_time': bet.bet_time.strftime('20%y-%m-%dT%H:%M:%S'),
                                'bet_status': bet.bet_status,
                                'bet_gain': bet.bet_gain
                            }
                            pusher_client.trigger(BET_CHANNEL, event, data)

    def interrupt_thread():
        global fetchingThread
        fetchingThread.cancel()

    def init_thread():
        global fetchingThread
        print('init background thread')
        fetchingThread = threading.Timer(POOL_TIME, fetch)
        fetchingThread.start()

    init_thread()
    atexit.register(interrupt_thread)

    return app


