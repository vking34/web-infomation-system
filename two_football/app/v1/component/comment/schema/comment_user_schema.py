from marshmallow import Schema, fields


class CommentUserSchema(Schema):
    user_id = fields.Integer(required=True)
    name = fields.String(required=True)
