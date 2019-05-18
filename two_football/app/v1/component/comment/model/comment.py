from app import db
import datetime
from sqlalchemy import desc
from app.v1.component.user.model.user import User


class Comment(db.Model):
    __tablename__ = 'comment'

    match_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    user = db.relation(User)
    time = db.Column(db.DATETIME, primary_key=True)
    comment = db.Column(db.String(300))

    def __init__(self, match_id, user_id, comment):
        self.match_id = match_id
        self.user_id = user_id
        self.time = datetime.datetime.now()
        self.comment = comment

    def save(self):
       db.session.add(self)
       db.session.commit()

    @classmethod
    def find_comments_of_match(cls, match_id, number):
        return cls.query.filter_by(match_id=match_id).order_by(desc('time')).limit(number).all()