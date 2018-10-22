#!/usr/bin/env python
#


import requests
import json
import argparse

parser = argparse.ArgumentParser(     description=__doc__)

parser.add_argument('-u','--GIT_USERNAME', nargs='+', type=str, dest='GIT_USERNAME', help="git userid", required=True)
parser.add_argument('-p','--GIT_PASSWORD', nargs='+', type=str, dest='GIT_PASSWORD', help="git password", required=True)
parser.add_argument('-o','--REPO_OWNER', nargs='+', type=str, dest='REPO_OWNER', help="Owner of repo", required=True)
parser.add_argument('-n','--REPO_NAME', nargs='+', type=str, dest='REPO_NAME', help="Name of repo", required=True)

args = parser.parse_args()
git_username = ''.join(args.GIT_USERNAME)
git_password = ''.join(args.GIT_PASSWORD)
repo_owner = ''.join(args.REPO_OWNER)
repo_name = ''.join(args.REPO_NAME)




print "Checking values....."
print git_username
print git_password
print repo_owner
print repo_name
#print "EMAIL_FROM:",email_from


def trigger_issue(title, body=None, labels=None):
    """Triggers an incident via the V2 REST API using sample data."""
    
    url = 'https://api.github.com/repos/%s/%s/issues' % (repo_owner, repo_name)
  
  # Create an authenticated session to create the issue
    session = requests.Session()
    session.auth = (git_username, git_password)
    # Create our issue
    issue = {'title': title,
             'body': body,
             'labels': labels}
    # Add the issue to our repository
    r = session.post(url, json.dumps(issue))
    if r.status_code == 201:
        print ('Successfully created Issue {0:s}'.format(title))
    else:
        print ('Could not create Issue {0:s}'.format(title))
        print ('Response:', r.content)

if __name__ == '__main__':
    trigger_issue('git title', 'git body', ['bug'])