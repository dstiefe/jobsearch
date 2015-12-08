import time
from flask import Flask, request, url_for, render_template, flash, redirect, url_for, request, abort, jsonify
from app import *
import flask
from itertools import groupby

""" http://blog.luisrei.com/articles/flaskrest.html
"""
from app import create
from app import delete
from app import retrieve
from app import update
from app import search
from flask import json
import os
import re
import sys
import os.path
from boto import dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from flask.ext.dynamo import Dynamo

# username: daniel
AWS_ACCESS_KEY_ID = 'AKIAJCSJR3BZJ62BMDVQ'
AWS_SECRET_ACCESS_KEY = '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'
REGION = 'us-east-1'

conn = dynamodb2.connect_to_region(
    REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

fields_userJob = ['username', 'firstname', 'lastname', 'accounttype']

fields_jobJob = ['job_id', 'job_title', 'job_location', 'published_date', 'job_description', 'job_requirements',
                 'about_us', 'job_snapshot', 'share', 'category', 'tags', 'employee_type']


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get_user', methods=['GET'])
def route_get_user():
    users = Table('jobUser', connection=conn)

    if 'username' in request.args:
        username = request.args.get('username')
        final_response = retrieve.get_user(username, users)
    else:
        final_response = {'status': '404', 'data': []}

    return jsonify(final_response)


@app.route('/get_job', methods=['GET'])
def route_get_job():
    jobs = Table('jobJobs', connection=conn)

    if 'jobid' in request.args:
        job_id = request.args.get('jobid')
        final_response = retrieve.get_job(job_id, jobs)
    else:
        final_response = {'status': '404', 'data': []}

    return jsonify(final_response)


@app.route('/filter_user', methods=['GET'])
def route_filter_user():
    users = Table('jobUser', connection=conn)
    list_arg = [(x[0], x[1][0]) for x in request.args.lists()]
    d = {}
    for item in list_arg:
        if item[0] in fields_userJob:
            d[item[0]] = item[1]

    final_response = search.filter_users(d, users)
    return jsonify(final_response)


@app.route('/filter_job', methods=['GET'])
def route_filter_job():
    jobs = Table('jobJobs', connection=conn)

    list_arg = [(x[0], x[1][0]) for x in request.args.lists()]
    d = {}
    for item in list_arg:
        if item[0] in fields_jobJob:
            d[item[0]] = item[1]
    final_response = search.filter_jobs(d, jobs)
    return jsonify(final_response)


@app.route('/jobs', methods=['GET'])
def route_filter_job_time():
    jobs = Table('jobJobs', connection=conn)

    list_arg = [(x[0], x[1][0]) for x in request.args.lists()]
    d = {}
    print(list_arg)
    for item in list_arg:
        if 'from' == item[0]:
            d[item[0]] = item[1]
        if 'to' == item[0]:
            d[item[0]] = item[1]
    if 'to' not in d.keys():
        d['to'] = 'now'
    final_response = search.filter_jobs_time(d, jobs)
    return jsonify(final_response)


@app.route('/create_user', methods=['POST'])
def route_create_user():
    users = Table('jobUser', connection=conn)
    if request.headers['Content-Type'] == 'application/json':
        data = json.dumps(request.json)
        print(data)
        final_response = create.create_user(data, users)
    else:
        final_response = {'status': '404', 'message': 'You need to specify data'}
    return jsonify(final_response)


@app.route('/create_job', methods=['POST'])
def route_create_job():
    jobs = Table('jobJobs', connection=conn)
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        print("tttt", type(data), data)
        final_response = create.create_job(data, jobs)
    else:
        final_response = {'status': '404', 'message': 'You need to specify data'}
    return jsonify(final_response)


@app.route('/delete_user', methods=['POST'])
def route_delete_user():
    users = Table('jobUser', connection=conn)
    if request.headers['Content-Type'] == 'application/json':
        data = json.loads(json.dumps(request.json))
        if data.get("username") != None:
            final_response = delete.delete_user(data.get("username"), users)
        else:
            final_response = {'status': '404', 'message': 'You need to specify data'}
    else:
        final_response = {'status': '404', 'message': 'You need to specify data'}
    return jsonify(final_response)


@app.route('/delete_job', methods=['POST'])
def route_delete_job():
    jobs = Table('jobJobs', connection=conn)
    if request.headers['Content-Type'] == 'application/json':
        data = json.loads(json.dumps(request.json))
        if data.get("job_id") != None:
            final_response = delete.delete_job(data.get("job_id"), jobs)
        else:
            final_response = {'status': '404', 'message': 'You need to specify data'}
    else:
        final_response = {'status': '404', 'message': 'You need to specify data'}

    return jsonify(final_response)


@app.route('/update_user', methods=['POST'])
def route_update_user():
    users = Table('jobUser', connection=conn)
    if request.headers['Content-Type'] == 'application/json':
        data = json.dumps(request.json)
        final_response = update.update_user(data, users)
    else:
        final_response = {'status': '404', 'message': 'You need to specify data'}
    return jsonify(final_response)


@app.route('/update_job', methods=['POST'])
def route_update_job():
    jobs = Table('jobJobs', connection=conn)
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        final_response = update.update_job(data, jobs)
    else:
        final_response = {'status': '404', 'message': 'You need to specify data'}
    return jsonify(final_response)
