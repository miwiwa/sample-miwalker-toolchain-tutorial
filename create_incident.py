#!/usr/bin/env python
#
# Copyright (c) 2016, PagerDuty, Inc. <info@pagerduty.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of PagerDuty Inc nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL PAGERDUTY INC BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import json
import argparse
from os import environ

#import requests

package = 'requests'

import pip

print("Importing requests")
pip.main(['install', package])

#def import_or_install(package):
#    try:
#        print("Attempting to import " + package)
#        __import__(package)
#    except ImportError:
#    	print("Attempting to install " + package)
#        pip.main(['install', package])

ids_job_name = environ.get('IDS_JOB_NAME')
ids_job_id = environ.get('IDS_JOB_ID')
ids_stage_name = environ.get('IDS_STAGE_NAME')
ids_project_name = environ.get('IDS_PROJECT_NAME')
workspace = environ.get('WORKSPACE')

toolchain_json = "%s/_toolchain.json" % workspace

with open(toolchain_json) as f:
    data = json.load(f)


parser = argparse.ArgumentParser(     description=__doc__)

#parser.add_argument('-a','--API_KEY', nargs='+', type=str, dest='API_KEY', help="PagerDuty API Key", required=True)
#parser.add_argument('-s','--SERVICE_ID', nargs='+', type=str, dest='SERVICE_ID', help="PagerDuty Service ID", required=True)
#parser.add_argument('-f','--EMAIL_FROM', nargs='+', dest='EMAIL_FROM', help="Add valid PagerDuty email address", required=True)
#parser.add_argument('-w','--WORKSPACE', nargs='+', type=str, dest='WORKSPACE', help="WORKSPACE for environment", required=True)

#args = parser.parse_args()
#api_key = ''.join(args.API_KEY)
#service_id = ''.join(args.SERVICE_ID)
#email_from=str(args.EMAIL_FROM)
#workspace = ''.join(args.WORKSPACE)



def trigger_incident():
    
    """Triggers an incident via the V2 REST API using sample data."""
    pd_service_id = [i['parameters']['service_id'] for i in data["services"] if 'pagerduty' in i['broker_id']]
    pd_api_key = [i['parameters']['api_key'] for i in data["services"] if 'pagerduty' in i['broker_id']]
    pd_user_email = [i['parameters']['user_email'] for i in data["services"] if 'pagerduty' in i['broker_id']]
    
    try:
      api_key = pd_api_key[0]
      service_id = pd_service_id[0]
      user_email = pd_user_email[0]
    except IndexError:
      print("ERROR: Pager Duty is not configured correctly with the toolchain")

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
            "title": "Job: " + ids_job_name + " in Stage: " + ids_stage_name + "failed" ,
            "service": {
                "id": service_id,
                "type": "service_reference"
            },
            "body": {
                "type": "incident_body",
                "details":  ids_job_name + "in project" + ids_project_name  + "failed"
            }
          }
        }

    r = requests.post(url, headers=headers, data=json.dumps(payload))

   
    code=r.status_code
    
    
    if code != 201:
    	print("ERROR: PagerDuty incident request did not complete successfully")
        exit()
    
    print r.json()

if __name__ == '__main__':
	#print("Installing request package")
	#import_or_install('requests')
	#print("performing recursive lookup")
	
	print("=============================")
	print("Creating incident report")
	trigger_incident()
