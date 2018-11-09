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
        '''POST Body should be like this:
        {
            "name": "Ferenc",
            "contact": "122222313111"
        }
        If user entered both required fields,then
        we add record to DB for this user '''
        if user_name and user_contact:
            status = db.Contacts.insert_one({
                "name" : user_name,
                "contact" : user_contact
            })
            return dumps({'message' : 'Succesfully recorded to DB'})
        else:
            return dumps({'message' : 'Record not created'})
    except Exception, e:
        return dumps({'error' : str(e)})


@app.route("/get_contact", methods = ['GET'])
def get_contact():
    try:
        if request.args:
            name = request.args
            data = db.Contacts.find_one(name)
            ''' If user entered a specific name like this:
            http://localhost:5000/get_contact?name=Ferenc
            we get record for this user '''
            if data:   
                return dumps(data)
            else:
                return dumps({'message' : 'Record not found'})
        else:
            ''' If user not entered a specific name like this:
            http://localhost:5000/get_contact
            we get all records from Contacts DB '''
            data = db.Contacts.find()
            return dumps(data)

    except Exception, e:
        return dumps({'error' : str(e)})

@app.route("/delete_contact", methods = ['DELETE'])
def delete_contact():
    try:
        if request.args:
            name = request.args
            data = db.Contacts.find_one(name)
            ''' If user entered a specific name like this:
            http://localhost:5000/delete_contact?name=Ferenc
            we delete this record from DB'''
            if data:
                db.Contacts.delete_one(name)   
                return dumps({'message' : 'Record deleted'})
            else:
                return dumps({'message' : 'Record not found'})

    except Exception, e:
        return dumps({'error' : str(e)})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')