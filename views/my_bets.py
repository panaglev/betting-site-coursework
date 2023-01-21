import os
import jwt
import sqlite3
from flask import request, abort
from flask_restx import Resource, Namespace

def auth_required(func): 
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        data = jwt.decode(token, os.environ.get('SECRET'), "HS256")
        if not data:
            abort(401)
        return func(*args, **kwargs)
    return wrapper

my_bets_ns = Namespace("my-bets")

@my_bets_ns.route("/")
class MyBetsView(Resource):
    """Returns all users bets"""
    @auth_required
    def get(self):
        user_bets = []
        token = request.cookies.get("token")
        data = jwt.decode(token, os.environ.get('SECRET'), "HS256")
        login = data['login']
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM users WHERE login = '%s';"%(login))
            user_id = cursor.fetchone()[0]
            res = cursor.execute("SELECT team1_id, team2_id, winner FROM events WHERE event_id IN (SELECT event_id FROM bets WHERE user_id = %d) AND event_status NOT null;"%(user_id))
            #return res.fetchall()
            res1 = cursor.execute("SELECT events.team1_id, events.team2_id, bets.assume_win FROM events, bets WHERE event_id IN (SELECT event_id FROM bets WHERE user_id = %d);"%(user_id))
            print(res1)
            for i in res1:
                team1, team2 = i
                cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(team1_id))
                team1 = cursor.fetchone()[0]
                cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(team2_id))
                team2 = cursor.fetchone()[0]
                user_bets.append(f"{team1} vs {team2} is in the progress")

            for i in res:
                team1_id, team2_id, winner = i
                cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(team1_id))
                team1 = cursor.fetchone()[0]
                cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(team2_id))
                team2 = cursor.fetchone()[0]
                if winner == 1:
                    user_bets.append(f"{team1} was playing against {team2} and {team1} won")
                else:
                    user_bets.append(f"{team1} was playing against {team2} and {team2} won")
        