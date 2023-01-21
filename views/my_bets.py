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

@my_bets_ns.route("/paid")
class MyBetsPaidView(Resource):
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
        return user_bets

@my_bets_ns.route("/active")
class MyBetsActiveVeiw(Resource):
    def get(self):
        user_bets = []
        token = request.cookies.get("token")
        data = jwt.decode(token, os.environ.get('SECRET'), "HS256")
        login = data['login']
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM users WHERE login = '%s';"%(login))
            user_id = cursor.fetchone()[0]
            res = cursor.execute("SELECT team1_id, team2_id FROM events WHERE event_id IN (SELECT event_id FROM bets WHERE user_id = %d);"%(user_id))
            print(res.fetchall())
            for i in res:
                team1_id, team2_id = i
                cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(team1_id))
                team1 = cursor.fetchone()[0]
                cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(team2_id))
                team2 = cursor.fetchone()[0]
                user_bets.append(f"In progress {team1} vs {team2}")
        return user_bets
