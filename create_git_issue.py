#!/usr/bin/env python
# Script will create a Git issue in specified repository passed in.  Currently only working with github.com


import requests
import json
import argparse

# Requires user to pass in 4 parameters:  Their Git username and password which must have read/write access to repo. In addition, the script
# requires the Git repo and owner names

parser = argparse.ArgumentParser(     description=__doc__)

parser.add_argument('-u','--GIT_USERNAME', nargs='+', type=str, dest='GIT_USERNAME', help="Git userid to repo that has read/write access", required=True)
parser.add_argument('-p','--GIT_PASSWORD', nargs='+', type=str, dest='GIT_PASSWORD', help="Git password to repo that has read/write access", required=True)
parser.add_argument('-o','--REPO_OWNER', nargs='+', type=str, dest='REPO_OWNER', help="Owner of repo to create issue in", required=True)
parser.add_argument('-n','--REPO_NAME', nargs='+', type=str, dest='REPO_NAME', help="Name of repo to create issue in", required=True)

args = parser.parse_args()
git_username = ''.join(args.GIT_USERNAME)
git_password = ''.join(args.GIT_PASSWORD)
repo_owner = ''.join(args.REPO_OWNER)
repo_name = ''.join(args.REPO_NAME)


def trigger_issue(title, body=None, labels=None):
    """Triggers an incident via the V2 REST API using sample data."""
    
    # Specifies URL for github api
    url = 'https://api.github.com/repos/%s/%s/issues' % (repo_owner, repo_name)
  
  	# Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (git_username, git_password)
   
  	# Create the issue
    issue = {'title': title,
             'body': body,
             'labels': lab
             els}
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