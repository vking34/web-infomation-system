from app import db
from app.v1.component.fixture.model.match import Match
from sqlalchemy import desc, asc


class Bet(db.Model):
    __tablename__ = 'bet'

    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('fixture.match_id'), primary_key=True)
    match = db.relation(Match)
    bet_type = db.Column(db.Integer, primary_key=True)
    bet_amount = db.Column(db.Integer, nullable=False)
    bet_content = db.Column(db.String(10), nullable=False)
    bet_time = db.Column(db.DATETIME)
    bet_status = db.Column(db.String(12))
    bet_gain = db.Column(db.Integer)

    def __init__(self, user_id, match_id, bet_type, bet_amount, bet_content, bet_time):
        self.user_id = user_id
        self.match_id = match_id
        self.bet_type = bet_type
        self.bet_amount = bet_amount
        self.bet_content = bet_content
        self.bet_time = bet_time
        self.bet_status = 'PROCESSING'
        self.bet_gain = 0

    def save(self):
        db.session.add(self)
        db.session.commit()

    def end(self, bet_gain):
        if bet_gain == 0:
            self.bet_status = 'LOSE'
        else:
            self.bet_gain = bet_gain
            self.bet_status = 'WIN'

        db.session.commit()

    @classmethod
    def find_bet(cls, user_id, match_id, bet_type):
        return cls.query.filter_by(user_id=user_id, match_id=match_id, bet_type=bet_type).first()

    @classmethod
    def find_bets_of_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).order_by(desc('bet_time')).all()

    @classmethod
    def find_bets_of_match(cls, match_id):
        return cls.query.filter_by(match_id=match_id).order_by(asc('bet_time')).all()

    @classmethod
    def find_user_bets_for_match(cls, match_id, user_id):
        return cls.query.filter_by(match_id=match_id, user_id=user_id).all()
