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

import requests
import json
import argparse

parser = argparse.ArgumentParser(     description=__doc__)

parser.add_argument('-a','--API_KEY', nargs='+', dest='API_KEY', help="PagerDuty API Key", required=True)

args = parser.parse_args()
api_key = args.API_KEY

print api_key

# Update to match your API key
API_KEY = 'Wd1wzzuFSzGm_Hx7KcU8'
SERVICE_ID = 'PCE74N6'
FROM = 'miwalker@us.ibm.com'

def trigger_incident():
    """Triggers an incident via the V2 REST API using sample data."""
    
    url = 'https://api.pagerduty.com/incidents'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.pagerduty+json;version=2',
        'Authorization': 'Token token={token}'.format(token=API_KEY),
        'From': FROM
    }

    payload = {
        "incident": {
            "type": "incident",
            "title": "Job: ${JOB_NAME} Stage: ${IDS_STAGE_NAME}",
            "service": {
                "id": SERVICE_ID,
                "type": "service_reference"
            },
            #"incident_key": "baf7cf21b1da41b4b0221008339ff3571",
            "body": {
                "type": "incident_body",
                "details": "${JOB_NUMBER} failed"
            }
          }
        }

    r = requests.post(url, headers=headers, data=json.dumps(payload))

    print 'Status Code: {code}'.format(code=r.status_code)
    print r.json()

if __name__ == '__main__':
    trigger_incident()