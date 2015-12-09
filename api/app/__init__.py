from datetime import timedelta

from flask import Flask
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from flask.ext.dynamo import Dynamo
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity


TABLE_PREFIX = 'JS'
TABLE_USERS = "{}_{}".format(TABLE_PREFIX, 'Users')
TABLE_JOBS = "{}_{}".format(TABLE_PREFIX, 'Jobs')
TABLE_RESUMES = "{}_{}".format(TABLE_PREFIX, 'Resumes')

app = Flask(__name__)
app.config['DYNAMO_TABLES'] = [
    Table(TABLE_USERS, schema=[HashKey('id')]),
    Table(TABLE_JOBS, schema=[HashKey('id')]),
    Table(TABLE_RESUMES, schema=[HashKey('id')]),
]
app.config['SECRET_KEY'] = '2283IP3JMMv1-HObk0_38d327B21Zp8u-gHmc_0ZA!CJj'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=864000)
app.config['JWT_AUTH_URL_RULE']  = '/api/v1/auth'

dynamo = Dynamo(app)
#with app.app_context():
#   dynamo.create_all()

from app.controllers.AuthController import *
jwt = JWT(app, authenticate, identity)
jwt.auth_response_callback = auth_response
api = Api(app)

from app.controllers.UsersController import *

api.add_resource(UsersController, '/api/v1/users')
api.add_resource(UserController, '/api/v1/users/<string:user_id>')


#from app import views

