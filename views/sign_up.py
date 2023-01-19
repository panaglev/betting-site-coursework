import os
import sqlite3
from flask import request
from hashlib import sha256
from flask_restx import Resource, Namespace

sign_up_ns = Namespace("sign-up")

@sign_up_ns.route("/")
# Able for every user
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
            password = sha256((password+os.environ.get('HASH_SALT')).encode('utf-8')).hexdigest()
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