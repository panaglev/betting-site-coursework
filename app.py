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
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()
            
    def post(self):
        req_json = request.get_json()
        print(req_json) # {'login': 'my_login', 'password': 'my_super_password'}
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            login = req_json["login"]
            password = req_json["password"]
            password = sha256((password+HASH_SALT).encode('utf-8')).hexdigest()
            #cursor.execute(f"INSERT INTO users (login, pass_hash, balance) VALUES ('{login}', '{password}', 0)")
            #cur.execute("SELECT * FROM userdata WHERE Name = %s;", (name,)) <- safe to do 
            cursor.execute("INSERT INTO users (login, pass_hash, balance) VALUES ('%s', '%s', 0);"%(login, password,))
            connection.commit()
        return "", 200

if __name__ == "__main__":
    app.run(debug=True)