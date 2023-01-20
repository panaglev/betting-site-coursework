import jwt
import sqlite3
from flask import request, abort
from flask_restx import Resource, Namespace

SECRET = "etg64vtah7r6atw74afiar6jtw4rsetrset69c8s"

def admin_required(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        data = jwt.decode(token, SECRET, "HS256")
        if data['login'] not in ("Admin"):
            abort(401)
        return func(*args, **kwargs)
    return wrapper

def moder_required(func):
    def wrapper(*args, **kwargs):
        token = request.cookies.get("token")
        data = jwt.decode(token, SECRET, "HS256")
        if data['login'] not in ("Admin", "Vasya_Mask_of_Madness", "Stalker_1337"):
            abort(401)
        return func(*args, **kwargs)
    return wrapper

utils_ns = Namespace("utils")

@utils_ns.route("/users") # moderators panel able to update and ban(delete) users, add events
# Admin and moderators
class UtilsUsers(Resource):
    @moder_required
    def get(self):
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall(), 200 # 200 - OK

    @moder_required
    def patch(self):
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor("UPDATE users SET balance = %d;"%(req_json["balance"]))
            connection.commit()
            return  "Successful", 200
       

@utils_ns.route("/events")
# Admin and moderators
class UtilsEvents(Resource):
    @moder_required
    def post(self):
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO events (team1_id, team2_id, event_status) VALUES (%d, %d, %d);"%(req_json["team1_id"], req_json["team2_id"], 1))
            return "", 201 # 201 - Created

@utils_ns.route("/<string:username>")
# Admin only
class CheckBalance(Resource):
    @admin_required
    def get(self, username):
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE login = '%s';"%(username))
            return cursor.fetchall()

@utils_ns.route("/payback")
# Admin only
class PaybackView(Resource):
    def get(self):
        pass
        # print all active bets just copy paste code from bets(I guess)

    @admin_required
    def post(self):
        """Steps:
        Close event -> click button -> script goes thrugh bets and compare data  with 2 loops

        1. Close event set winner and change event_status 
        2. Script goes for sql selecting bet's where event_id of this event
        3. Collect team1 bet amount and team2 bet amount
        4. Calculate profits in %
        5. Compare to the winning one
        (if yes - add money to balance)
        (if no - just do nothing)

        1. Iterate trught bets and calculate amount betted on team1 and team2 
        2. Calculate profits in %
        3. Iterate second time trught checking for assume_win

        1. Grab all bets with mentioned event_id 
        2. Divide the winners and losers(on step 1 in 2 different lists)
        3. Grab all money amount(back in step one, can be done by one query)
        4. Calculate %'s
        5. Second time iterate trught user's betted and if """
        with sqlite3.connect("coursework.db") as connection:
            amount1 = 0
            amount2 = 0
            req_json = request.get_json() # event_id, winner
            cursor = connection.cursor()
            #cursor.execute("UPDATE events SET winner = %d;"%(req_json["winner"]))
            cursor.execute("UPDATE evets SET winner = %d WHERE event_id = %d"%(req_json['winner'], req_json['event_id'])) 
            cursor.execute("UPDATE events SET event_status= 2 WHERE event_id = %d;"%(req_json['event_id']))

            cursor.execute("SELECT * FROM bets WHERE event_id = %d;"%(req_json['event_id']))
            res = cursor.fetchall()
            for i in res:
                _, _, _, assume_win, bet_amount = res
                if assume_win == 1:
                    amount1 += bet_amount
                else:
                    amount2 += bet_amount

           # team 1 = 1234
           # team 2 = 753 
           # if team 1 won = 1 + 753/1234 = 1.61 
           # if team 2 won = 1 + 1234/753 = 2.63