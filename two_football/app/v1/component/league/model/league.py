from app import db


class League(db.Model):
    __tablename__ = 'league'

    league_id = db.Column(db.Integer, primary_key=True)
    league_name = db.Column(db.String(60), nullable=False)
    country = db.Column(db.String(60), nullable=False)

    @classmethod
    def find_leagues(cls):
        return cls.query.all()
