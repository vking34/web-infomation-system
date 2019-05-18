from marshmallow import Schema, fields, validate


class CardSchema(Schema):
    code = fields.String(validate=validate.Regexp('^[a-zA-Z0-9]{16}$'), required=True)
    password = fields.String(validate=validate.Length(min=6), required=True)
