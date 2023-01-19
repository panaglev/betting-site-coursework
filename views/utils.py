import sqlite3
from flask import request
from flask_restx import Resource, Namespace

utils_ns = Namespace("utils")

@utils_ns.route("/users") # moderators panel able to update and ban users, add events
# Able for admin and moderators
class UtilsUsers(Resource):
    def get(self):
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall(), 200 # 200 - OK

    def patch(self):
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor("UPDATE users SET balance = %d;"%(req_json["balance"]))
            connection.commit()
            return  "Successful", 200
       

@utils_ns.route("/events")
# Able for admin and moderators
class UtilsEvents(Resource):
    def get(self):
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM events")
            return cursor.fetchall()

    def post(self):
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO events (team1_id, team2_id, event_status) VALUES (%d, %d, %d);"%(req_json["team1_id"], req_json["team2_id"], 1))
            return "", 201 # 201 - Created