#!/usr/bin/env python
# Program submits PagerDuty incidents or Git issues upon request

import pip
package = 'requests'
pip.main(['install', package])

import requests
import json
import argparse
from os import environ
import subprocess
import re

# Read in argument(s)
description = 'Specify creation of incident/issue in Pagerduty and Git Issues'
   
parser = argparse.ArgumentParser(     description=__doc__)
parser.add_argument('-a','--ALERTS', nargs='+', type=str.lower, dest='ALERTS', help="Enter 'PagerDuty' and/or 'Git' to open incident/issue", required=True)

args = parser.parse_args()
alerts = args.ALERTS

print("alerts:",alerts)

# Import Pipeline environment variables 
ids_job_name = environ.get('IDS_JOB_NAME')
ids_job_id = environ.get('IDS_JOB_ID')
ids_stage_name = environ.get('IDS_STAGE_NAME')
ids_project_name = environ.get('IDS_PROJECT_NAME')
ids_url = environ.get('IDS_URL')
workspace = environ.get('WORKSPACE')

# Load toolchain json to dict for parsing
toolchain_json = "%s/_toolchain.json" % workspace

with open(toolchain_json) as f:
    data = json.load(f)

print(type(data))

ids_region_id = [data[i]['services']['region_id'] for i in data]
ids_instance_id = [data[i]['services']['instance_id'] for i in data]
 
print("ids_region_id:", ids_region_id)
print("ids_instance_id:", ids_instance_id)


def trigger_incident():
	# Function creates request to create new PagerDuty incident and submits
    
    # Parse dict for PagerDuty parameters 
    pd_service_id = [i['parameters']['service_id'] for i in data["services"] if 'pagerduty' in i['broker_id']]
    pd_api_key = [i['parameters']['api_key'] for i in data["services"] if 'pagerduty' in i['broker_id']]
    pd_user_email = [i['parameters']['user_email'] for i in data["services"] if 'pagerduty' in i['broker_id']]
    
    # Retrieve values from resulting list. If values do not exist then 
    try:
      api_key = pd_api_key[0]
      service_id = pd_service_id[0]
      user_email = pd_user_email[0]
    except IndexError:
      print("ERROR: Pager Duty is not configured correctly with the toolchain")
	
	# Develop request to create incident through API
    url = 'https://api.pagerduty.com/incidents'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={token}'.format(token=api_key),
        'From': user_email
    }

    payload = {
        "incident": {
            "type": "incident",
            "title": "Job: " + ids_job_name + " in Stage: " + ids_stage_name + " failed" ,
            "service": {
                "id": service_id,
                "type": "service_reference"
            },
            "body": {
                "type": "incident_body",
                "details":  ids_url
            }
          }
        }
	
	# Send request to PagerDuty
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    
    code=r.status_code
    
    # Check if request was successful. If not successful then fail the job   
    if code != 201:
    	print("ERROR: PagerDuty incident request did not complete successfully")
        exit()
    else:
		print("ERROR: PagerDuty incident request created successfully")
		
def trigger_issue(title, body=None, labels=None):
	# Function creates request to create Git Issue and submits
   
    # Retrieve values necessary to submit request through Git API.
    # Note: Values not available in toolchain.json
    git_remote_url = subprocess.check_output(['git','config','--get','remote.origin.url'],stderr= subprocess.STDOUT)
    pattern = re.compile(r"//|:|@")
    git_parameters = pattern.split(git_remote_url)
    git_username = git_parameters[2]
    git_password = git_parameters[3]
	
	# Retrieve owner and name of repo from toolchain.json
    repo_owner = [i['parameters']['owner_id'] for i in data["services"] if 'github' in i['broker_id']]
    repo_name = [i['parameters']['repo_name'] for i in data["services"] if 'github' in i['broker_id']]
    
    try:
      git_repo_owner = repo_owner[0]
      git_repo_name = repo_name[0]
    except IndexError:
      print("ERROR: Git Issues is not configured correctly with the toolchain")

    # Specifies URL for github api
    url = 'https://api.github.com/repos/%s/%s/issues' % (git_repo_owner, git_repo_name)
  
  	# Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (git_username, git_password)
   
  	# Create the issue
    issue = {'title': title,
             'body': body,
             'labels': labels}
    
    # Post the issue to the Git repository
    r = session.post(url, json.dumps(issue))
    
    if r.status_code != 201:
    	print ('Could not create Git Issue {0:s}'.format(title))
        exit()   
    else:
        print ('Successfully created Git Issue {0:s}'.format(title))
        
	 

if __name__ == '__main__':	
	print("=============================")
	print("Creating alerts")
	
	if all(alert_type in alerts for alert_type in ('incident', 'issue')):
		print("Creating PagerDuty incident....")
		trigger_incident()
		print("Creating Git issue....")
		trigger_issue("Job: " + ids_job_name + " in Stage: " + ids_stage_name + " failed", ids_url, ['bug'])	
	elif 'incident' in alerts:		
		trigger_incident()
	elif 'issue' in alerts:
		trigger_issue("Job: " + ids_job_name + " in Stage: " + ids_stage_name + " failed", ids_url, ['bug'])
	else:
		print("Alert type was not specified in call")

	