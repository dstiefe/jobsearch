
import boto 

def get_user(username,jobUser):
	status = 200
	r_json= {}
	try:
		if username != 'all':
			item = jobUser.get_item(username=username)
			r_json['username'] = item['username']
			r_json['first_name'] = item['first_name']
			r_json['last_name'] = item['last_name']
			r_json['account_type'] = item['account_type']
			r_response = {'status': status, 'data': [r_json]}
		elif username == 'all':
			data = [] 
			names = jobUser.scan()
			for item in names:
				r_json= {}
				r_json['username'] = item['username']
				r_json['first_name'] = item['first_name']
				r_json['last_name'] = item['last_name']
				r_json['account_type'] = item['account_type']
				data += [r_json]
			r_response = {'status': status, 'data': data}
		else: 
			status= 404
			r_response = {'status': status, 'data': []}

	except:
		status= 404
		r_response = {'status': status, 'data': []}

	return r_response

def get_job(jobid,jobJobs):
	status = 200
	r_json= {}
	try:
		if jobid != 'all':
			item = jobJobs.get_item(job_id=jobid)
			# Getting data 
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
			r_response = {'status': status, 'data': [r_json]}
		elif jobid == 'all':
			all_jobs = jobJobs.scan()
			data = []
			for item in all_jobs:
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
		else: 
			status= 404
			r_response = {'status': status, 'data': []}
	except:
		status= 404
		r_response = {'status': status, 'data': []}
	return r_response

