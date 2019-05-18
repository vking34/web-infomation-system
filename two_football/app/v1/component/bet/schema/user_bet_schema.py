from marshmallow import Schema, fields, validate


class UserBetSchema(Schema):
    user_id = fields.Integer(required=True)
    # match_id = fields.Integer(required=True)

    bet_type = fields.Integer(required=True)
    bet_amount = fields.Integer(required=True)
    bet_content = fields.String(required=True)
    bet_time = fields.Time(required=True)
    bet_status = fields.String(required=True)
    bet_gain = fields.Integer(required=True)
