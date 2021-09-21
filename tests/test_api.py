import json
import pprint
import requests

# pwd="9Qmrn6amB"
api_key = "testtesttest"
headers = {"Authorization": api_key}

# get all chores
r = requests.get("http://127.0.0.1:8000/api/chores",
                 headers=headers)
pprint.pprint(json.loads(r.content))

# get specific chore
r = requests.get("http://127.0.0.1:8000/api/chores",
                 headers=headers,
                 json={"chore_id": "259823"})
pprint.pprint(json.loads(r.content))

# add a chore
r = requests.post(
    "http://127.0.0.1:8000/api/create_chore",
    headers=headers,
    json= \
        {
            "chore_name": "Test API Chore",
            "category": "Coding",
            "type": "recurring",
            "alert_days": 3
        }
)
pprint.pprint(r.content)

chore_id = 259824

# edit a chore
r = requests.post(
    "http://127.0.0.1:8000/api/edit_chore",
    headers=headers,
    json= \
        {
            "chore_id": chore_id,
            "chore_name": "Test API Chore UPDATED",
            "category": "Coding",
            "type": "recurring",
            "alert_days": 3
        }
)
print(r.content)

# delete a chore
r = requests.post(
    "http://127.0.0.1:8000/api/delete_chore",
    headers=headers,
    json= \
        {
            "chore_id": chore_id,
            "chore_name": "Test API Chore UPDATED",
            "category": "Coding",
            "type": "recurring",
            "alert_days": 3
        }
)
print(r.content)
