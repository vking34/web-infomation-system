from marshmallow import Schema, fields, validate
from marshmallow.validate import Range
from app.v1.component.fixture.schema.match_schema import MatchSchema


class BetSchema(Schema):
    user_id = fields.Integer(required=True)
    # match_id = fields.Integer(required=True)
    match = fields.Nested(MatchSchema)
    bet_type = fields.Integer(validate=[Range(min=1, max=3)], required=True)
    bet_amount = fields.Integer(validate=[Range(min=1)], required=True)
    bet_content = fields.String(validate=validate.Regexp('^([0-9]{1,2}-[0-9]{1,2}|[0-9])$'), required=True)
    bet_time = fields.Time(required=True)
    bet_status = fields.String(required=True)
    bet_gain = fields.Integer(required=True)
