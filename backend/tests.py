import json
import pprint
import requests

# GET ALL TODOS
r = requests.get("http://127.0.0.1:8000/todos")
pprint.pprint(json.loads(r.content))

# ADD A TODOITEM
r = requests.post(
    "http://127.0.0.1:8000/todos",
    json= \
        {"name": "rake the leaves",
         "days_until_alert": 7}

)
pprint.pprint(r.content)


# GET ALL TODOS AGAIN
r = requests.get("http://127.0.0.1:8000/todos")
pprint.pprint(json.loads(r.content))
