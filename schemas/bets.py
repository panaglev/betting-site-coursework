from marshmallow import Schema, fields

class BetSchema(Schema): # sport, team1 name, team2 name, amount bet on team1, amount bet on team2
    sport = fields.Str()
    team1 = fields.Str()
    team2 = fields.Str()
    betTeam1Amount = fields.Integer()
    betTeam2Amount = fields.Integer()