import os
import jwt
import sqlite3
from flask import request, abort
from flask_restx import Resource, Namespace

def moder_required(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        data = jwt.decode(token, os.environ.get('SECRET'), "HS256")
        if data['login'] not in ("Admin", "Vasya_Mask_of_Madness", "Stalker_1337"):
            abort(401)
        return func(*args, **kwargs)
    return wrapper

team_ns = Namespace("teams")

@team_ns.route("/")
class TeamsViews(Resource):
    @moder_required
    def get(self):
        teams_list = []
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT team_id, team_name FROM teams")
            res = cursor.fetchall()
            for i in res:
                team_id, team_name = i
                teams_list.append(f"{team_id}. {team_name}")

        return teams_list, 200 # 200 - OK