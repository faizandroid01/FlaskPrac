from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import json

# base Constructor
app = Flask(__name__)
# Resource Addition to API For App
api = Api(app)
# setup mongo
client = MongoClient("mongodb://db:27017")
# setup mongo db name
db = client.newDb
# create collection
users = db["users"]


# For Mapping Users
#  similar as gson in java
class User(object):
    username = ""
    name = ""
    password = ""
    age = ""


def as_user(d):
    u = User()
    u.__dict__.update(d)
    return u


# Response Model
class Response(object):
    responseCode = ""
    msg = ""

    def __init__(self, responseCode, msg):
        self.responseCode = responseCode
        self.msg = msg


# Resource to register
class RegisterUser(Resource):
    body = request.get_json()
    user = json.loads(body, object_hook=as_user)

    # search in db for , if user exist
    user_exist(user)

    # saving user in db
    users.insert({"username": user.username, "name": user.name, "password": user.password, "age": user.age})


def user_exist(user):
    user_exists = users.find({"username": user.username})
    if len(user_exists) > 0:
        return jsonify(Response(301, "user already exists"))
