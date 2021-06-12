import json
import requests

# get all chores
headers = {"Authorization": "5Kp8SUJbm"}
r = requests.get("http://127.0.0.1:8000/api/chores", headers=headers)
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

# Header tests
