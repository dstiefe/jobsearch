import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

def delete_user(username, jobUser):
	try:
		jobUser.delete_item(username=username)
		status=200
		r_response = {'status': status, 'message': 'data has been erased'}
	except:
		status=400
		r_response = {'status': status, 'message': 'we couldn t delete the data'}
	return r_response


def delete_job(job_id, jobJobs):
	try:
		jobJobs.delete_item(job_id=job_id)
		status=200
		r_response = {'status': status, 'message': 'data has been erased'}
	except:
		status=400
		r_response = {'status': status, 'message': 'we couldn t delete the data'}
	return r_response

