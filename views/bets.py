import os
import json
import sqlite3
from hashlib import sha256
from flask_restx import Api, Resource, Namespace
from flask import Flask, request, jsonify

bets_ns = Namespace("bets")

@bets_ns.route("/") # display all active bets
# Able to all users event not authorized
class BetsView(Resource):
    def get(self):
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM bets")
            return jsonify(cursor.fetchall()), 200 # 200 - OK
            
    def post(self): # change to create bet 
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            login = req_json["login"]
            password = req_json["password"]
            password = sha256((password+os.environ.get('HASH_SALT')).encode('utf-8')).hexdigest()
            cursor.execute("INSERT INTO users (login, pass_hash, balance) VALUES ('%s', '%s', 0);"%(login, password,))
            connection.commit()
        return "", 201 # 201 - Created

@bets_ns.route("/history")
# Able to authorized users
class MyBetsView(Resource): # rework to more complex sql query -> less code 
    def get(self):
        list_bets = []
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()

            #cursor.execute("SELECT events.team1_id, events.team2_id, events.event_status, events.winner, teams.team_id, teams.sport_id, teams.team_name, sports.sport_id, sports.sport_type FROM events, teams, sports WHERE events.team1_id = teams.team_id;")
            cursor.execute("SELECT team1_id, team2_id, winner FROM events WHERE winner NOT NULL")
            for column1, column2, column3 in cursor.fetchall():
                inter = []
                cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(column1))
                inter.append(cursor.fetchone())
                cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(column2))
                inter.append(cursor.fetchone())
                if column3 == 1:
                    cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(column1))
                    inter.append(cursor.fetchone())
                else:
                    cursor.execute("SELECT team_name FROM teams WHERE team_id = %d;"%(column2))
                    inter.append(cursor.fetchone())
                list_bets.append(inter)
                inter = []
            return json.dumps(list_bets)