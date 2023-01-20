import os
import sqlite3
from hashlib import sha256
from functools import wraps 
from flask import request, jsonify
from flask_restx import Resource, Namespace

HASH_SALT= "9fc47da85894433819877a9d0e3f01f6ff35afeb25cc6058d138284abd3a050b"

sign_in_ns = Namespace("sign-in")

@sign_in_ns.route("/")
# Able for every user
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
            #password = sha256((password+os.environ.get('HASH_SALT')).encode('utf-8')).hexdigest()
            password = sha256((password+HASH_SALT).encode('utf-8')).hexdigest()
            # Check if user exists or not
            cursor.execute("SELECT * FROM users WHERE login = '%s' and pass_hash = '%s';"%(login, password,))
            if cursor.fetchall() != []:
                return "Access gained", 200 # 200 - OK
            else:
                return "Such user already exists or password is incorrect", 401 # 401 - Unauthorized