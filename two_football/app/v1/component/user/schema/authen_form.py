from marshmallow import Schema, fields, validate


class AuthenticationForm(Schema):
    username = fields.String(validate=validate.Regexp('^(?=.{6,100}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$', 0,
                                                      'Not a valid username'),
                             required=True)
    password = fields.String(validate=validate.Length(min=6), required=True)
