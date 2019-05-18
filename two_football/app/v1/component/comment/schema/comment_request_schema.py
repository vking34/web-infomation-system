from marshmallow import Schema, fields, validate
from marshmallow.validate import Regexp


class CommentRequestSchema(Schema):
    comment = fields.String(validate=Regexp('^.{1,300}$'), required=True)
