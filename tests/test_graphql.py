import json
import pprint
import requests

# pwd="9Qmrn6amB"
api_key = "ulbuBSEt6"
headers = {"Authorization": api_key}

# get all chores
r = requests.post("http://127.0.0.1:8000/graphql",
                 data={
                     "query": "hello"
                 },
                 headers={
                     "Content-Type": "application/json"
                 }
                 # headers=headers
                 )

pprint.pprint(json.loads(r.content))
