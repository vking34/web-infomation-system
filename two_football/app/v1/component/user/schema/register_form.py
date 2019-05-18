from marshmallow import Schema, fields, validate


class RegisterFormSchema(Schema):
    username = fields.String(validate=validate.Regexp('^(?=.{6,100}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$', 0,
                                                      'Not a valid username'),
                             required=True)
    password = fields.String(validate=validate.Length(min=6), required=True)
    name = fields.String(validate=validate.Length(min=2, max=100), required=True)
    phone = fields.String(validate=validate.Regexp('^0+([0-9]{9})$', 0,
                                                   'Not a valid phone number. A valid phone number consists 10 digits and starts with 0.'),
                          required=True)
    email = fields.Email(required=True)
