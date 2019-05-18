from marshmallow import Schema, fields, validate
from marshmallow.validate import Range


class BetRequestSchema(Schema):
    bet_type = fields.Integer(validate=[Range(min=1, max=3, error='Not negative')], required=True)
    bet_amount = fields.Integer(validate=[Range(min=1, error='> 1')], required=True)
    bet_content = fields.String(validate=validate.Regexp('^([0-9]{1,2}-[0-9]{1,2}|[0-9])$'), required=True)
