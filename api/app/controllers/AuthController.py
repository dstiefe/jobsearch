from app import *
from werkzeug.security import safe_str_cmp
from flask_restful import Resource, abort, reqparse
from app.models.User import User
from flask_jwt import JWT, jwt_required, current_identity
from flask import Flask, jsonify, request
import hashlib
import boto
from app.helpers.helpermethods import *

def auth_response(access_token, identity):
    return jsonify({'access_token': access_token.decode('utf-8'), 'user_id': identity.id, "account_type": identity.account_type})



def authenticate(username, password):

    exist_items = dynamo.tables[TABLE_USERS].scan(user_name__eq=username, limit = 1)
    exist_item = get_first(exist_items)
    if exist_item is not None:
        exist_item = User(**exist_item)

    if exist_item and safe_str_cmp(exist_item.password, hashlib.md5(password).hexdigest()):
        return exist_item


def identity(payload):
    user_id = payload['identity']

    try:
        exist_item = dynamo.tables[TABLE_USERS].get_item(id=user_id)
    except boto.dynamodb2.exceptions.ItemNotFound:
        exist_item = None

    return User(**exist_item)

def roles_required(dict):
    def role_permission_in(function_to_decorate):

        def a_wrapper_accepting_arguments(*args):
            print(dict)
            account_type=current_identity.account_type
            if account_type not in dict:
                abort(401)
            function_to_decorate(*args)

        return a_wrapper_accepting_arguments
    return role_permission_in


