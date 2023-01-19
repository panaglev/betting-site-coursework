import os
import jwt
import sqlite3
import datetime
from hashlib import sha256
from functools import wraps 
from flask import request, jsonify
from flask_restx import Resource, Namespace

sign_in_ns = Namespace("sign-in")
secret = "somesecretvaluetogeneratetoken"

#def token_required(f):
#    @wraps(f)
#    def decorated(*args, **kwargs):
#        token = request.args.get('token')
#
#        if not token:
#            return jsonify({"message":"Token is missing"}), 403
#
#        try:
#            data = jwt.decode(token, secret)
#        except:
#            return jsonify({"message": "Invalid token"}), 403
#    return decorated

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
            password = sha256((password+os.environ.get('HASH_SALT')).encode('utf-8')).hexdigest()
            # Check if user exists or not
            cursor.execute("SELECT * FROM users WHERE login = '%s' and pass_hash = '%s';"%(login, password,))
            if cursor.fetchall() != []:
                token = jwt.encode({"login":login, "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, secret)
                return jsonify({"token":token}) # 200 - OK
            else:
                return "Such user already exists or password is incorrect", 401 # 401 - Unauthorized