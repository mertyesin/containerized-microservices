from flask import Flask
from flask import request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
import json

client = MongoClient('mongodb:27017')
db = client.ContactDB

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

@app.route("/add_contact", methods = ['POST'])
def add_contact():
    try:
        data = json.loads(request.data)
        user_name = data['name']
        user_contact = data['contact']
        if user_name and user_contact:
            status = db.Contacts.insert_one({
                "name" : user_name,
                "contact" : user_contact
            })
        return dumps({'message' : 'SUCCESS'})
    except Exception, e:
        return dumps({'error' : str(e)})


@app.route("/get_contact/", methods = ['GET'])
def get_contact():
    s = db.Contacts.find_one({'name' : "repo"})

    if s:
      output = {'name' : s['name'], 'contact' : s['contact']}
    else:
      output = "No such name"
    return jsonify({'result' : output})


# from flask import Flask
# from flask import jsonify
# from flask import request
# from flask_pymongo import PyMongo
# from bson.json_util import dumps
# import json

# client = MongoClient('localhost:27017')
# db = client.ContactDB

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Flask Dockerized'


# mongo = PyMongo(app)

# @app.route('/star', methods=['GET'])
# def get_all_stars():
#   print ("get_all_stars")
#   star = mongo.db.stars
#   output = [
#         {
#             'name':'Mert',
#             'distance': '15245'
#         }
#   ]
#   # for s in star.find():
#   #   output.append({'name' : s['name'], 'distance' : s['distance']})
#   return jsonify({'result' : output})

# @app.route("/add_contact", methods = ['POST'])
# def add_contact():
#     try:
#         data = json.loads(request.data)
#         user_name = data['name']
#         user_contact = data['contact']
#         if user_name and user_contact:
#             status = db.Contacts.insert_one({
#                 "name" : user_name,
#                 "contact" : user_contact
#             })
#         return dumps({'message' : 'SUCCESS'})

#     except Exception, e:
#         return dumps({'error' : str(e)})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

# # @app.route('/star/', methods=['GET'])
# # def get_one_star(name):
# #   star = mongo.db.stars
# #   s = star.find_one({'name' : name})
# #   if s:
# #     output = {'name' : s['name'], 'distance' : s['distance']}
# #   else:
# #     output = "No such name"
# #   return jsonify({'result' : output})


# # if __name__ == '__main__':
# #     app.run(debug=True)
