import os
import jwt
import sqlite3
from flask import request, abort
from flask_restx import Resource, Namespace

def admin_required(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        data = jwt.decode(token, os.environ.get('SECRET'), "HS256")
        if data['login'] not in ("Admin"):
            abort(401)
        return func(*args, **kwargs)
    return wrapper

def moder_required(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        data = jwt.decode(token, os.environ.get('SECRET'), "HS256")
        if data['login'] not in ("Admin", "Vasya_Mask_of_Madness", "Stalker_1337"):
            abort(401)
        return func(*args, **kwargs)
    return wrapper

def auth_required(func): 
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        data = jwt.decode(token, os.environ.get('SECRET'), "HS256")
        if not data:
            abort(401)
        return func(*args, **kwargs)
    return wrapper

utils_ns = Namespace("utils")

@utils_ns.route("/users")
class UtilsUsers(Resource):
    @moder_required
    def get(self):
        """List all users"""
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall(), 200 # 200 - OK

    @moder_required
    def patch(self):
        """Set a balance to some user(alternative deposit)"""
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor("UPDATE users SET balance = %d;"%(req_json["balance"]))
            connection.commit()
            return  "Successful", 200
       
@utils_ns.route("/events")
class UtilsEvents(Resource):
    @moder_required
    def post(self):
        """Create event"""
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO events (team1_id, team2_id, event_status) VALUES (%d, %d, %d);"%(req_json["team1_id"], req_json["team2_id"], 1))
            return "", 201 # 201 - Created

@utils_ns.route("/payback")
class PaybackView(Resource):
    admins_profit = 0
    @admin_required
    def post(self):
        """Pay when event was over"""
        global admins_profit
        with sqlite3.connect("coursework.db") as connection:
            amount1 = 0
            amount2 = 0
            req_json = request.get_json()
            cursor = connection.cursor()
            cursor.execute("UPDATE events SET winner = %d WHERE event_id = %d"%(req_json['winner'], req_json['event_id'])) 
            cursor.execute("UPDATE events SET event_status = %d WHERE event_id = %d;"%(2, req_json['event_id']))

            cursor.execute("SELECT * FROM bets WHERE event_id = %d;"%(req_json['event_id']))
            res = cursor.fetchall()
            for i in res:
                _, _, _, assume_win, bet_amount = i
                if assume_win == 1:
                    amount1 += bet_amount
                else:
                    amount2 += bet_amount

            admins_profit = 0
            admins_profit += (amount1 + amount2)

            payback_coef = 0.0
            if req_json['winner'] == 1:
                payback_coef = 1 + (round(amount2/amount1, 2) - 0.05) # money formula
            else:
                payback_coef = 1 + (round(amount1/amount2, 2) - 0.05) # money formula
        
            for i in res:
                _, _, user_id, assume_win, bet_amount = i
                if assume_win == req_json['winner']:
                    admins_profit -= to_pay
                    cursor.execute("SELECT balance FROM users WHERE user_id = %d;"%(user_id))
                    balance = cursor.fetchone()[0]
                    to_pay += balance
                    to_pay = bet_amount * payback_coef
                    #cursor.execute("UPDATE users SET balance %f WHERE user_id = %d")
                    cursor.execute(f"UPDATE users SET balance = {to_pay} WHERE user_id = {user_id}") # FIX WHEN FIND PLACEHOLDER FOR REAL NUMBER 
                else:
                    continue

        return admins_profit, 201
    
@utils_ns.route("/admin-profit")
class ProfitView(Resource):
    @admin_required
    def get(self):
        """See site profit"""
        global admins_profit
        return admins_profit

@utils_ns.route("/balance")
class GetBalanceView(Resource):
    @auth_required
    def get(self):
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor() 
            token = request.cookies.get("token")
            data = jwt.decode(token, os.environ.get('SECRET'), "HS256")
            cursor.execute("SELECT balance FROM users WHERE login = '%s';"%(data['login']))
            return cursor.fetchone()[0]
