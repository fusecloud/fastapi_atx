import json
import requests

# GET ALL TODOS
r = requests.get("http://127.0.0.1:8000/todos")
print(json.loads(r.content))

# ADD A TODOITEM
r = requests.post(
    "http://127.0.0.1:8000/todos",
    json= \
        {"name": "take out trash",
         "days_until_alert": 7}

)
print(r.content)
