from functools import wraps

import boto
from flask_restful import Resource, abort, reqparse
from flask import Flask, jsonify, request
from app import *
from flask_jwt import JWT, jwt_required, current_identity
import uuid
from app.models.User import User
from flask.views import MethodView
import hashlib
from app.helpers.helpermethods import *




class UserController(Resource):
    @jwt_required()
    def get(self, user_id):
        print '%s' % current_identity
        try:
            if user_id == 'me':
                user_id = current_identity.id
            exist_item = dynamo.tables[TABLE_USERS].get_item(id=user_id)
            exist_item = User(**exist_item)

        except boto.dynamodb2.exceptions.ItemNotFound:
            exist_item = None

        return jsonify(exist_item.__dict__)



class UsersController(Resource):



    @jwt_required()
    def put(self):
        user_id = current_identity.id

        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, location=('json'), required=False)
        parser.add_argument('last_name', type=str, location=('json'), required=False)
        parser.add_argument('password', type=str, location=('json'), required=False)
        args = parser.parse_args()

        firstname = args.get('first_name')
        lastname = args.get('last_name')
        password = args.get('password')


        try:
            exist_item = dynamo.tables[TABLE_USERS].get_item(id=user_id)
        except boto.dynamodb2.exceptions.ItemNotFound:
            exist_item = None

        if exist_item is None:
            abort(404, message="User not found!")

        if firstname is not None:
            exist_item['first_name'] = firstname

        if lastname is not None:
            exist_item['last_name'] = lastname

        if password is not None:
            exist_item['password'] = hashlib.md5(password).hexdigest()

        exist_item.save(overwrite=True)

        return exist_item, 200

    @jwt_required()
    def delete(self):
        try:
            dynamo.tables[TABLE_USERS].delete_item(id=current_identity.id)
        except boto.dynamodb2.exceptions.ItemNotFound:
            abort(404, message="User not found!")
        return None, 204

    @jwt_required()
    #@role_permission(['admin'])
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, location=('args'), required=False)
        args = parser.parse_args()
        username = args.get('username')

        if username is None:
            users = dynamo.tables[TABLE_USERS].scan()
        else:
            users = dynamo.tables[TABLE_USERS].scan(user_name__eq=username)

        return users, 200

    def post(self):

        json_data = request.get_json(force=True)

        username = json_data['user_name']
        firstname = json_data['first_name']
        lastname = json_data['last_name']
        password = json_data['password']

        exist_items = dynamo.tables[TABLE_USERS].scan(user_name__eq=username, limit = 1)
        exist_item = get_first(exist_items)
        if exist_item is not None:
            abort(400, message="User already registered!")


        user = User(str(uuid.uuid4()), username, firstname, lastname, hashlib.md5(password).hexdigest())
        dynamo.tables[TABLE_USERS].put_item(data=user.__dict__)

        response = jsonify(user.__dict__)
        response.status_code = 201 #https://github.com/mitsuhiko/flask/issues/478
        return response
