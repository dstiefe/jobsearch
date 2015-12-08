import boto.dynamodb2
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER

import json


def update_user(d, jobUser):
	data= json.loads(json.dumps(json.loads(d)))
	print(data, type(data))
	if data.get("username") != None:
		try:
			r_json = {}
			item = jobUser.get_item(username=data.get("username"))
			#jobUser.delete_item(username=data.get("username"))
			for k,v in data.items():
				item[k]= v
			item.save(overwrite=True)
			r_response = {'status': status, 'message': 'updated'}
		except:
			status=400
			r_response = {'status': status, 'message': 'update'}
	else:
		status=400
		r_response = {'status': status, 'message': 'update'}
	
	return r_response

def update_job(d, jobJob):
	data= json.loads(json.dumps(d))
	if data.get("job_id") != None:
		try:
			item = jobJob.get_item(job_id=data.get("job_id"))
			for k,v in data.items():
				item[k]= v
			item.save(overwrite=True)
			r_response = {'status': status, 'message': 'data has been updated'}
		except:
			status=400
			r_response = {'status': status, 'message': 'check the results'}
	else:
		status=400
		r_response = {'status': status, 'message': 'check the results'}
	
	return r_response




