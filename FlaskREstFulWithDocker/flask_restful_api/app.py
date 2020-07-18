from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

# base Constructor
app = Flask(__name__)
# Resource Addition to API For App
api = Api(app)
# setup mongo
client = MongoClient("mongodb://db:27017")

# setup mongo db name
db = client.newDb
# create collection
UserNum = db["user_num"]

# insert into collection
UserNum.insert({"user_num": 0})


@app.route('/')
def indexRoute():
    str = 'HelloWorld'
    val = {"str": str}
    return jsonify(val)


@app.route('/calculateSumThroughNormalFlask', methods=['POST', 'GET'])
def calculateSumThroughNormalFlask():
    if request.method == 'POST':
        body = request.get_json()
        x = int(body["x"])
        y = int(body["y"])

        z = {"sum": (x + y)}
        return z, 200

    if request.method == 'GET':
        response = Response("Method GET is unavailable.")
        return response.getMsg()


# using flask_restful

class Add(Resource):
    @staticmethod
    def post():
        body = request.get_json()
        if "x" in body and "y" in body:
            x = int(body["x"])
            y = int(body["y"])

            z = {"sum": (x + y)}
            return z, 200
        else:
            return


class Visit(Resource):
    @staticmethod
    def get():
        prev_no_of_users = UserNum.find({})[0]["user_num"]
        new_no_of_users = prev_no_of_users + 1
        UserNum.update({}, {"$set": {"user_num": new_no_of_users}})
        return str("Hi User, Visitor No :" + str(new_no_of_users))


# include Add class with the api in a restful way
api.add_resource(Add, '/calculateSumThroughRestfulFlask')
api.add_resource(Visit, "/visit")


class Response:
    msg = ''

    def __init__(self, msg):
        self.msg = msg

    def getMsg(self):
        return self.msg


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
