import os
import jwt
import sqlite3
import datetime
from hashlib import sha256
from flask import request
from flask_restx import Resource, Namespace

HASH_SALT= "9fc47da85894433819877a9d0e3f01f6ff35afeb25cc6058d138284abd3a050b"
SECRET = "etg64vtah7r6atw74afiar6jtw4rsetrset69c8s"

sign_in_ns = Namespace("sign-in")

@sign_in_ns.route("/")
# Free access
class SignInView(Resource):
    def post(self):
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            password = sha256((req_json['password']+HASH_SALT).encode('utf-8')).hexdigest()
            print(password)
            cursor.execute("SELECT * FROM users WHERE login = '%s' and pass_hash = '%s';"%(req_json['login'], password))
            if cursor.fetchall() != []:
                token = jwt.encode({'login':req_json['login'], 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, SECRET)
                return "", 200, {'Set-Cookie': f'token={token}'} # 200 - OK
            else:
                return "Username or password is incorrect", 401 # 401 - Unauthorized