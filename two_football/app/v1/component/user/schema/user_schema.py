from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    user_id = fields.Integer(required=True)
    username = fields.String(required=True)
    # password = fields.String()
    role = fields.String(required=True)
    balance = fields.Integer(required=True)
    name = fields.String(required=True)
    picture = fields.String()
    phone = fields.String(validate=validate.Length(min=9, max=10))
    email = fields.Email()


class UpdatingProfileSchema(Schema):
    name = fields.String(validate=validate.Length(min=2, max=100), required=True)
    phone = fields.String(validate=validate.Regexp('^0+([0-9]{9})$', 0,
                                                   'Not a valid phone number. A valid phone number consists 10 digits and starts with 0.'),
                          required=True)
    email = fields.Email(required=True)
