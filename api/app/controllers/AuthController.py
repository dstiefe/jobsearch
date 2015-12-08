from app import *
from werkzeug.security import safe_str_cmp
from app.models.User import User
from flask_jwt import JWT, jwt_required, current_identity
from flask import Flask, jsonify, request
import hashlib
import boto

def auth_response(access_token, identity):
    return jsonify({'access_token': access_token.decode('utf-8'), 'user_id': identity.id, "account_type": identity.account_type})



def authenticate(username, password):
    try:
        exist_item = dynamo.tables[TABLE_USERS].get_item(user_name=username)
        exist_item = User(**exist_item)
    except boto.dynamodb2.exceptions.ItemNotFound:
        exist_item = None

    if exist_item and safe_str_cmp(exist_item.password, hashlib.md5(password).hexdigest()):
        return exist_item


def identity(payload):
    user_id = payload['identity']

    try:

        exist_items = dynamo.tables[TABLE_USERS].scan(id__eq=user_id, limit = 1)
        exist_item = get_first(exist_items)
    except boto.dynamodb2.exceptions.ItemNotFound:
        exist_item = None

    return User(**exist_item)


def get_first(iterable, default=None):
    if iterable:
        for item in iterable:
            return item
    return None
