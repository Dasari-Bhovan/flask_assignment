from flask import Flask
from flask_restful import Api, Resource, reqparse
from pymongo import MongoClient
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

app = Flask(__name__)
api = Api(app)

# Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')
# Connect to MongoDB
client = MongoClient('mongodb://host.docker.internal:27017/')
db = client['userdb']
collection = db['users']


class UsersResource(Resource):
    def get(self):
        users = list(collection.find())
        return users, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, required=True)
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        user = {
            '_id': args['id'],
            'name': args['name'],
            'email': args['email'],
            'password': args['password']
        }
        try:
            result = collection.insert_one(user)
        except DuplicateKeyError:
            return "User ID already exists. Please change the user ID.", 500
        return 'User created successfully', 201


class UserResource(Resource):
    def get(self, user_id):
        user = collection.find_one({'_id': user_id})
        if user:
            return user, 200
        else:
            return 'User not found', 404

    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        updated_user = {
            'name': args['name'],
            'email': args['email'],
            'password': args['password']
        }
        result = collection.update_one({'_id': user_id}, {'$set': updated_user})
        if result.modified_count > 0:
            return 'User updated successfully', 200
        else:
            return 'User not found', 404
    def delete(self, user_id):
        result = collection.delete_one({'_id': user_id})
        if result.deleted_count > 0:
            return 'User deleted successfully', 200
        else:
            return 'User not found', 404

class UserAgeResource(Resource):
    def get(self, user_id, age):
        # Handle logic for user_id and age combination
        # return {'user_id': user_id, 'age': age}, 200
        pass


api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')
api.add_resource(UserAgeResource, '/users/<int:user_id>/<int:age>')


if __name__ == '__main__':
    app.run()
