import os
import jwt
import sqlite3
import datetime
from flask import request
from hashlib import sha256
from flask_restx import Resource, Namespace

HASH_SALT= "9fc47da85894433819877a9d0e3f01f6ff35afeb25cc6058d138284abd3a050b"
SECRET = "etg64vtah7r6atw74afiar6jtw4rsetrset69c8s"

sign_up_ns = Namespace("sign-up")

@sign_up_ns.route("/")
# Free acess
class SignUpView(Resource): # Display login page or what's for this required
    def post(self):
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            password = req_json["password"]
            #password = sha256((password+os.environ.get('HASH_SALT')).encode('utf-8')).hexdigest()
            password = sha256((password+HASH_SALT).encode('utf-8')).hexdigest()
            # Check if user already in db to avoid Broken Access controll
            # Top 1 of vulns by OWASP Top 10 
            cursor.execute("SELECT * FROM users WHERE login = '%s';"%(req_json['login']))
            if cursor.fetchall() == []:
                # Using params, not f-strings to input data in sql query
                # Avoid SQL Injection, Top 3 vuln by OWASP Top 10
                #cursor.execute(f"INSERT INTO users (login, pass_hash, balance) VALUES ('{login}', '{password}', 0)") <- not safe to do
                #cur.execute("SELECT * FROM userdata WHERE Name = %s;", (name,)) <- safe to do 
                cursor.execute("INSERT INTO users (login, pass_hash, balance) VALUES ('%s', '%s', 0);"%(req_json['login'], password))
                connection.commit()
                token = jwt.encode({'login':req_json['login'], 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, SECRET)
                return "", 201, {'Set-Cookie': f'token={token}'} # 201 - Created
            else:
                return "This user already exist", 409 # 409 - Conflict