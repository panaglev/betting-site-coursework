import os
import jwt
import jinja2
import sqlite3
import datetime
from hashlib import sha256
from flask_restx import Resource, Namespace
from flask import request, render_template, make_response, abort

def auth_required(func): 
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        data = jwt.decode(token, os.environ.get('SECRET'), "HS256")
        if not data:
            abort(401)
        return func(*args, **kwargs)
    return wrapper

bets_ns = Namespace("bets")

@bets_ns.route("/")
class BetsView(Resource):
    @auth_required
    def get(self):
        """Return all active bets"""
        active_bets = []
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT event_id, team1_id, team2_id FROM events WHERE event_status = 1")
            res = cursor.fetchall()
            for i in res:
                event_id, team1_id, team2_id = i
                cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(team1_id))
                team1 = cursor.fetchone()[0]
                cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(team2_id))
                team2 = cursor.fetchone()[0]
                active_bets.append(f"Event id {event_id}: {team1} vs {team2}")
            return active_bets, 200
                
            
    @auth_required
    def post(self):
        """Allowes to bet on one of active bets"""
        req_json = request.get_json()
        token = request.cookies.get("token")
        data = jwt.decode(token, os.environ.get('SECRET'), "HS256")
        #if data['exp'] > int(datetime.datetime.utcnow()):
        if True:
            with sqlite3.connect("coursework.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM users WHERE login = '%s';"%(data['login']))
                user_id = cursor.fetchone()[0]
                cursor.execute("SELECT balance FROM users WHERE user_id = %d;"%(user_id))
                balance = cursor.fetchone()[0]
                if balance >= req_json['bet_amount']:
                    cursor.execute("UPDATE users SET balance = %d WHERE user_id = %d;"%(balance-float(req_json['bet_amount']), user_id))
                    cursor.execute("INSERT INTO bets (event_id, user_id, assume_win, bet_amount) VALUES (%d, %d, %d, %d);"%(req_json['event_id'], user_id, req_json['assume_win'], req_json['bet_amount']))
                    connection.commit()
                else:
                    return {"message":"Not enough money on balance to make a bet"}, 409 # 409 - Conflict

                return {"message":"Successfull"}, 201 # 201 - Created
        else:
            # FIX TOKEN EXP 
            return {"message":"Token has expired, please re-login"}, 401 # 401 - Unauthorized

@bets_ns.route("/history")
class MyBetsView(Resource): 
    def get(self):
        """All bets being played"""
        users_bets = []
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT event_id, team1_id, team2_id, winner FROM events WHERE winner IS NOT NULL")
            res = cursor.fetchall()
            for item in res:
                amount1 = 0
                amount2 = 0
                event_id, team1_id, team2_id, winner = item
                cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(team1_id))
                team1 = cursor.fetchone()[0]
                cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(team2_id))
                team2 = cursor.fetchone()[0]
                if winner == 1:
                    cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(team1_id))
                    winner = cursor.fetchone()[0]
                else:
                    cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(team2_id))
                    winner = cursor.fetchone()[0]
                cursor.execute("SELECT bet_amount FROM bets WHERE assume_win = 1 AND event_id = %d;"%(event_id))
                tmp = cursor.fetchall()
                for i in tmp:
                    for j in i:
                        amount1 += j
                cursor.execute("SELECT bet_amount FROM bets WHERE assume_win = 2 AND event_id = %d;"%(event_id))
                tmp = cursor.fetchall()
                for i in tmp:
                    for j in i:
                        amount2 += j
                #users_bets.append([team1, team2, amount1, amount2, winner]) 
                users_bets.append(f"{team1} has total amount of {amount1} and {team2} has total amount of {amount2}. The winner is {winner}")
            return users_bets
            #headers = {'Content-Type': 'text/html'}
            #return make_response(render_template("table.html", bets=["Thundra", "Navi", 500, 300, "Tundra"]), 200, headers)