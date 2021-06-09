import json
import requests

# get all chores
r = requests.get("http://127.0.0.1:8000/api/chores")
print(json.loads(r.content))

# add a chore
r = requests.post(
    "http://127.0.0.1:8000/api/chores",
    json= \
        {
            "title": "Walk Dog",
            "content": "BLah"
        }
)
print(r.content)
