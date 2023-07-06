from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
app = Flask(__name__)

# Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')
# Connect to MongoDB
client = MongoClient('mongodb://host.docker.internal:27017/')

db = client['userdb']
collection = db['users']
@app.route("/",methods=['GET'])
def hello():
    return "hi",200

# Endpoint to get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = list(collection.find())
    return jsonify(users), 200


# Endpoint to get a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = collection.find_one({'_id': user_id})
    if user:
        return jsonify(user), 200
    else:
        return 'User not found', 404


# Endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = {
        '_id': int(data['id']),
        'name': data['name'],
        'email': data['email'],
        'password': data['password']
    }
    try:
        result = collection.insert_one(user)
    except DuplicateKeyError:
        return "User Id already exists, change the user id",500
    return 'User created successfully', 201


# Endpoint to update a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    updated_user = {
        'name': data['name'],
        'email': data['email'],
        'password': data['password']
    }
    result = collection.update_one({'_id': user_id}, {'$set': updated_user})
    if result.modified_count > 0:
        return 'User updated successfully', 200
    else:
        return 'User not found', 404


# Endpoint to delete a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = collection.delete_one({'_id': user_id})
    if result.deleted_count > 0:
        return 'User deleted successfully', 200
    else:
        return 'User not found', 404


if __name__ == '__main__':
    app.run()
