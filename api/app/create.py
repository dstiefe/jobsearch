import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

import json


def create_user(d, jobUser):
	try:
		user=jobUser.get_item(username=username)
		status=400
		r_response = {'status': status, 'message': 'data already in the table'}
 			
	except:
		status=200
		data= json.loads(d)
		jobUser.put_item(data={
 			'username': data.get('username'),
			'first_name': data.get('firstname'),
			'last_name': data.get('lastname'),
			'account_type': 'standard_user'})
		r_response = {'status': status, 'message': 'data has been added'}

	return r_response


def create_job( d, jobJobs):
	data= json.loads(json.dumps(d))

	try:

		job=jobJobs.get_item(job_id=data.get('job_id'))
		status=400
		r_response = {'status': status, 'message': 'data already in the table'}
	except:
		status=200
		jobJobs.put_item(data={  'job_id': data.get('job_id'), 'job_title': data.get('job_title'),'job_location': data.get('job_location'),'published_date': data.get('published_date'),'job_description': data.get('job_description'),'job_requirements':  data.get('job_requirements'),'about_us': data.get('about_us'),'job_snapshot': data.get('job_snapshot'),'share': data.get('share'),'category':data.get('category'),'tags':data.get('tags'),'employee_type': data.get('employee_type')})
		r_response = {'status': status, 'message': 'data has been added'}
	return r_response


