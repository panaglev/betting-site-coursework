import sqlite3
from flask import request, abort
from flask_restx import Resource, Namespace

edit_bets_ns = Namespace("edit-bets")

@edit_bets_ns.route("/")
# Able to admin only! 
class AdminEditBetsView(Resource):
    def get(self):
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM bets")
            return cursor.fetchall(), 200 # 200 - OK

    def patch(self):
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE events SET winner = %d;"%(req_json["winner"]))