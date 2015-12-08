import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER
import datetime

def filter_jobs(creteria, jobJobs):
	status= 200
	all_jobs = jobJobs.scan()
	data = []
	found = False
	for item in all_jobs:
		for k,v  in creteria.items():
			print(k,v)
			if k == 'job_location' and v in item.get(k):
				found = True
			elif item.get(k) == v: 
				found = True

			if found: 
				r_json= {}
				r_json['job_id'] = item['job_id']
				r_json['job_title'] = item['job_title']
				r_json['job_location'] = item['job_location']
				r_json['published_date'] = item['published_date']
				r_json['job_description'] = item['job_description']
				r_json['job_requirements'] = item['job_requirements']
				r_json['about_us'] = item['about_us']
				r_json['job_snapshot'] = item['job_snapshot']
				r_json['share'] = item['share']
				r_json['category'] = item['category']
				r_json['tags'] = item['tags']
				r_json['employee_type'] = item['employee_type']
				data += [r_json]
				found = False

	r_response = {'status': status, 'data': data}
	return r_response

def filter_users(creteria, jobUser):
	status= 200
	all_users = jobUser.scan()
	data = []
	for item in all_users:
		for k,v  in creteria.items():
			if item.get(k) == v: 
				r_json= {}
				r_json['username'] = item['username']
				r_json['first_name'] = item['first_name']
				r_json['last_name'] = item['last_name']
				r_json['account_type'] = item['account_type']
				data += [r_json]
	r_response = {'status': status, 'data': data}
	return r_response


def filter_jobs_time(creteria, jobJobs):
	status= 200
	all_jobs = jobJobs.scan()
	data = []
	
	from_time= datetime.datetime.strptime(creteria['from'], "%m/%d/%Y")
	
	if creteria['to'] != 'now':
		to_time=datetime.datetime.strptime(creteria['to'], "%m/%d/%Y")
	else: 
		to_time = datetime.datetime.now()
	for item in all_jobs:
		job_time=datetime.datetime.strptime(item['published_date'], "%m/%d/%Y")
		if from_time < job_time < to_time:
			print(creteria['from'], creteria['to'])
			r_json= {}
			r_json['job_id'] = item['job_id']
			r_json['job_title'] = item['job_title']
			r_json['job_location'] = item['job_location']
			r_json['published_date'] = item['published_date']
			r_json['job_description'] = item['job_description']
			r_json['job_requirements'] = item['job_requirements']
			r_json['about_us'] = item['about_us']
			r_json['job_snapshot'] = item['job_snapshot']
			r_json['share'] = item['share']
			r_json['category'] = item['category']
			r_json['tags'] = item['tags']
			r_json['employee_type'] = item['employee_type']
			data += [r_json]

	r_response = {'status': status, 'data': data}
	return r_response
