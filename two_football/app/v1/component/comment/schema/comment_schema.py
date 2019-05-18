from marshmallow import Schema, fields, validate
from .comment_user_schema import CommentUserSchema


class CommentSchema(Schema):
    user = fields.Nested(CommentUserSchema)
    comment = fields.String(required=True)
    time = fields.Time(required=True)
