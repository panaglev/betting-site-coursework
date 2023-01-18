import sqlite3
from flask import Flask, request
from flask_restx import Api, Resource
from hashlib import sha256
import os
import json

app = Flask(__name__)
api = Api(app)
#HASH_SALT = "9fc47da85894433819877a9d0e3f01f6ff35afeb25cc6058d138284abd3a050b"
HASH_SALT = os.environ.get('HASH_SALT') # Best practice not to save confidential information in format like above 

#@api.route("/moderator") # moderators panel able to ban users, add events

@api.route("/bets") # display all active bets
class BetsView(Resource):
    def get(self):
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM bets")
            return cursor.fetchall(), 200 # 200 - OK
            
    def post(self): # change to create bet 
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            login = req_json["login"]
            password = req_json["password"]
            password = sha256((password+HASH_SALT).encode('utf-8')).hexdigest()
            cursor.execute("INSERT INTO users (login, pass_hash, balance) VALUES ('%s', '%s', 0);"%(login, password,))
            connection.commit()
        return "", 201 # 201 - Created

@api.route("/bets/history")
class MyBetsView(Resource):
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


@api.route("/my-bets")
class MyBetsView(Resource):
    def get(self):
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            #cursor.execute("SELECT team1_id, team2_id, winner FROM events WHERE event_id IN (SELECT event_id FROM betsevents WHERE bets_id IN (SELECT bet_id FROM bets where user_id = 2))")
            cursor.execute("SELECT * FROM bets WHERE user_id = 2")
            for event_id in cursor.fetchall():
                cursor.execute("SELECT * FROM events WHERE event_id = %d;"%(event_id[1]))
                print(cursor.fetchall())

@api.route("/admin/add_bets") # admin panel able to list users, add events
class AdminAddBetsView(Resource):
    def get(self):
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM bets")
            return cursor.fetchall(), 200 # 200 - OK

    def post(self):
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO events (team1_id, team2_id, event_status) VALUES (%d, %d, %d);"%(req_json["team1_id"], req_json["team2_id"], 1))
            return "", 201 # 201 - Created

@api.route("/admin/edit_bets")
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


@api.route("/sign-in")
class SignInView(Resource):
    def get(self):
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users") # Display login page
            return cursor.fetchall()

    def post(self):
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            login = req_json["login"]
            password = req_json["password"]
            password = sha256((password+HASH_SALT).encode('utf-8')).hexdigest()
            # Check if user exists or not
            cursor.execute("SELECT * FROM users WHERE login = '%s' and pass_hash = '%s';"%(login, password,))
            if cursor.fetchall() != []:
                return "", 200 # 200 - OK
            else:
                return "No such user or password is incorrect", 401 # 401 - Unauthorized
            

@api.route("/sign-up")
class SignUpView(Resource): # Display login page or what's for this required
    def get(self):
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users") 
            return cursor.fetchall()

    def post(self):
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            # Parse data from json 
            login = req_json["login"]
            password = req_json["password"]
            password = sha256((password+HASH_SALT).encode('utf-8')).hexdigest()
            # Check if user already in db to avoid Broken Access controll
            # Top 1 of vulns by OWASP Top 10 
            cursor.execute("SELECT * FROM users WHERE login = '%s';"%(login,))
            if cursor.fetchall() == []:
                # Using params, not f-strings to input data in sql query
                # Avoid SQL Injection, Top 3 vuln by OWASP Top 10
                #cursor.execute(f"INSERT INTO users (login, pass_hash, balance) VALUES ('{login}', '{password}', 0)") <- not safe to do
                #cur.execute("SELECT * FROM userdata WHERE Name = %s;", (name,)) <- safe to do 
                cursor.execute("INSERT INTO users (login, pass_hash, balance) VALUES ('%s', '%s', 0);"%(login, password,))
                connection.commit()
                return "", 201 # 201 - Created
            else:
                return "This user already exist", 409 # 409 - Conflict

if __name__ == "__main__":
    app.run(debug=True)