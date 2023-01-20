import sqlite3
from flask_restx import Resource, Namespace

my_bets_ns = Namespace("my-bets")

@my_bets_ns.route("/")
class MyBetsView(Resource):
    """Returns all users bets"""
    def get(self):
        user_bets = []
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            res = cursor.execute("SELECT team1_id, team2_id, winner FROM events WHERE event_id IN (SELECT event_id FROM bets WHERE user_id = 2) AND event_status NOT None") # parse user id from jwt and one more sql query
            print(res.fetchall())