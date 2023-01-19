import sqlite3
from flask_restx import Resource, Namespace

my_bets_ns = Namespace("my-bets")

@my_bets_ns.route("/")
class MyBetsView(Resource):
    def get(self):
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            #cursor.execute("SELECT team1_id, team2_id, winner FROM events WHERE event_id IN (SELECT event_id FROM betsevents WHERE bets_id IN (SELECT bet_id FROM bets where user_id = 2))")
            cursor.execute("SELECT * FROM bets WHERE user_id = 2")
            for event_id in cursor.fetchall():
                cursor.execute("SELECT * FROM events WHERE event_id = %d;"%(event_id[1]))
                print(cursor.fetchall())