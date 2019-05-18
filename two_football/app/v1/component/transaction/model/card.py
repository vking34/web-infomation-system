from app import db


class Card(db.Model):
    __tablename__ = 'card'

    code = db.Column(db.String(16), primary_key=True)
    value = db.Column(db.Integer(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)

    def load(self):
        self.active = False
        db.session.commit()



    @classmethod
    def find_card_by_code(cls, code):
        return cls.query.filter_by(code=code).first()
