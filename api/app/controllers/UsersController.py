import boto
from flask_restful import Resource, abort
from flask import Flask, jsonify, request
from app import *
from flask_jwt import JWT, jwt_required, current_identity
import uuid
from app.models.User import User
from flask.views import MethodView
import hashlib

class UsersController(Resource):
    #    def get(self, id):
    #        return {todo_id: todos[todo_id]}

    #    def delete(self, id):
    #        abort_if_todo_doesnt_exist(todo_id)
    #        del TODOS[todo_id]
    #        return '', 204
    @jwt_required()
    def get(self, user_id):
        print '%s' % current_identity
        try:
            exist_item = dynamo.tables[TABLE_USERS].get_item(user_name=user_id)
            exist_item = User(**exist_item)

        except boto.dynamodb2.exceptions.ItemNotFound:
            exist_item = None

        return jsonify(exist_item.__dict__)

    def post(self):

        json_data = request.get_json(force=True)

        username = json_data['user_name']
        firstname = json_data['first_name']
        lastname = json_data['last_name']
        password = json_data['password']

        try:
            dynamo.tables[TABLE_USERS].get_item(user_name = username)
            abort(400, message="User already registered!")

        except boto.dynamodb2.exceptions.ItemNotFound:

            user = User(str(uuid.uuid4()), username, firstname, lastname, hashlib.md5(password).hexdigest())
            dynamo.tables[TABLE_USERS].put_item(data=user.__dict__)

            response = jsonify(user.__dict__)
            response.status_code = 201 #https://github.com/mitsuhiko/flask/issues/478
            return response
