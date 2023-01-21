import os
import jwt
import sqlite3
import datetime
from flask import request
from hashlib import sha256
from flask_restx import Resource, Namespace

sign_up_ns = Namespace("sign-up")

@sign_up_ns.route("/")
class SignUpView(Resource):
    """Let to unauthorized user to register and recieve token"""
    def post(self):
        req_json = request.get_json()
        with sqlite3.connect("coursework.db") as connection:
            cursor = connection.cursor()
            password = sha256((req_json['password']+os.environ.get('HASH_SALT')).encode('utf-8')).hexdigest()

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
                token = jwt.encode({'login':req_json['login'], 'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, os.environ.get('SECRET'))
                return "", 201, {'Set-Cookie': f'token={token}'} # 201 - Created
            else:
                return {"message":"This user already exist"}, 409 # 409 - Conflict