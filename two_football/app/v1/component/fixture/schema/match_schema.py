from marshmallow import Schema, fields, validate


class MatchSchema(Schema):
    match_id = fields.Integer(required=True)
    league_id = fields.Integer(required=True)
    match_date = fields.String(required=True)
    match_time = fields.String(required=True)
    match_hometeam_name = fields.String(required=True)
    match_awayteam_name = fields.String(required=True)
    match_hometeam_halftime_score = fields.Integer(required=True)
    match_awayteam_halftime_score = fields.Integer(required=True)
    match_hometeam_score = fields.Integer(required=True)
    match_awayteam_score = fields.Integer(required=True)
    yellow_card = fields.Integer(required=True)
    match_status = fields.String(required=True)
