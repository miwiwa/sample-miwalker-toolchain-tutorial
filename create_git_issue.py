#!/usr/bin/env python
# Script will create a Git issue in specified repository passed in.  Currently only working with github.com


#import requests
import json
import argparse
import subprocess
from os import environ
import re


package = 'requests'

import pip

pip.main(['install', package])

print("Importing requests")

import requests
import subprocess

ids_job_name = environ.get('IDS_JOB_NAME')
ids_job_id = environ.get('IDS_JOB_ID')
ids_stage_name = environ.get('IDS_STAGE_NAME')
ids_project_name = environ.get('IDS_PROJECT_NAME')
ids_url = environ.get('IDS_URL')
workspace = environ.get('WORKSPACE')

toolchain_json = "%s/_toolchain.json" % workspace

with open(toolchain_json) as f:
    data = json.load(f)

# Requires user to pass in 4 parameters:  Their Git username and password which must have read/write access to repo. In addition, the script
# requires the Git repo and owner names

#parser = argparse.ArgumentParser(     description=__doc__)

#parser.add_argument('-u','--GIT_USERNAME', nargs='+', type=str, dest='GIT_USERNAME', help="Git userid to repo that has read/write access", required=True)
#parser.add_argument('-p','--GIT_PASSWORD', nargs='+', type=str, dest='GIT_PASSWORD', help="Git password to repo that has read/write access", required=True)
#parser.add_argument('-o','--REPO_OWNER', nargs='+', type=str, dest='REPO_OWNER', help="Owner of repo to create issue in", required=True)
#parser.add_argument('-n','--REPO_NAME', nargs='+', type=str, dest='REPO_NAME', help="Name of repo to create issue in", required=True)

#args = parser.parse_args()
#git_username = ''.join(args.GIT_USERNAME)
#git_password = ''.join(args.GIT_PASSWORD)
#repo_owner = ''.join(args.REPO_OWNER)
#repo_name = ''.join(args.REPO_NAME)




def trigger_issue(title, body=None, labels=None):
   
    git_remote_url = subprocess.check_output(['git','config','--get','remote.origin.url'],stderr= subprocess.STDOUT)

    pattern = re.compile(r"//|:|@")
    git_parameters = pattern.split(git_remote_url)
    print(type(git_parameters))
    print(git_parameters)

    git_username = git_parameters[2]
    git_password = git_parameters[3]

    print("git_username: " + git_username)
    print("git_password: " + git_password)
    repo_owner = [i['parameters']['owner_id'] for i in data["services"] if 'pagerduty' in i['broker_id']]
    repo_name = [i['parameters']['repo_name'] for i in data["services"] if 'pagerduty' in i['broker_id']]
    #pd_github = [i['parameters'] for i in data["services"] if 'github' in i['broker_id']]
    #print("pd_github: ", pd_github)

    try:
      git_repo_owner = repo_owner[0]
      git_repo_name = repo_name[0]
    except IndexError:
      print("ERROR: Pager Duty is not configured correctly with the toolchain")

    # Specifies URL for github api
    url = 'https://api.github.com/repos/%s/%s/issues' % (git_repo_owner, git_repo_name)
  
  	# Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (git_username, git_password)
   
  	# Create the issue
    issue = {'title': title,
             'body': body,
             'labels': labels}
    # Add the issue to the Git repository
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        print ('Successfully created Issue {0:s}'.format(title))
        print ('Response:', r.content)
    else:
        print ('Could not create Issue {0:s}'.format(title))
        print ('Response:', r.content)

if __name__ == '__main__':
    trigger_issue('git title', 'git body', ['bug'])