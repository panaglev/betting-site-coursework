import sqlite3
from flask import Flask, request
from flask_restx import Api, Resource
from hashlib import sha256

app = Flask(__name__)
api = Api(app)
HASH_SALT = "9fc47da85894433819877a9d0e3f01f6ff35afeb25cc6058d138284abd3a050b"

@api.route("/bets")
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