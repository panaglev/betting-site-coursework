import os
import jwt
import sqlite3
import datetime
from hashlib import sha256
from flask import request
from flask_restx import Resource, Namespace

log_in_ns = Namespace("log-in")

@log_in_ns.route("/")
class SignInView(Resource):
    """Let registered user to log in"""
    def post(self):
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            password = sha256((password+os.environ.get('HASH_SALT')).encode('utf-8')).hexdigest()
            
            # Check if the user exists
            cursor.execute("SELECT * FROM users WHERE login = '%s' and pass_hash = '%s';"%(req_json['login'], password))
            if cursor.fetchall() != []:
                token = jwt.encode({'login':req_json['login'], 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, os.environ.get('SECRET'))
                return "", 200, {'Set-Cookie': f'token={token}'} # 200 - OK
            else:
                return "Username or password is incorrect", 401 # 401 - Unauthorized