import json
import pprint
import requests

api_key = "testtesttest"
headers = {
    "Authorization": api_key,
    "Content-Type": "application/json"
}

# QUERIES
# Get user and/or chore data
query = \
    '''
    {
      user_chores {
        user_name
        occupation
        email
        chore_id
        chore_name
        type
        alert_days
      }
    }
    '''

# get all chores
r = requests.post(
    "http://127.0.0.1:8000/graphql",
    json={"query": query},
    headers=headers
)

pprint.pprint(json.loads(r.content))

# MUTATIONS
# Add a chore

mutation = \
    '''
    mutation {
        create_chore(
            chore_name: "TEST GraphQL"
            category: "Dev"
            type: "one-time"
            alert_days: 1
        ) {
            chore {
                user_id
                chore_name
                category
                type
            }
            ok
        }
    }
    '''

r = requests.post(
    "http://127.0.0.1:8000/graphql",
    json={"query": mutation},
    headers=headers
)

pprint.pprint(json.loads(r.content))

# Edit a chore
mutation = \
    '''
    mutation {
        edit_chore(
            chore_id: 259825
            chore_name: "TEST GraphQL-UPDATED"
            category: "Dev-UPDATED"
            type: "one-time-UPDATED"
            alert_days: 1
        ) {
            chore {
                user_id
                chore_name
                category
                type
            }
            ok
        }
    }
    '''

r = requests.post(
    "http://127.0.0.1:8000/graphql",
    json={"query": mutation},
    headers=headers
)

pprint.pprint(json.loads(r.content))

# remove a chore
mutation = \
    '''
    mutation {
        remove_chore(
            chore_id: 259825
        ) {
            ok
        }
    }
    '''

r = requests.post("http://127.0.0.1:8000/graphql",
                  json={
                      "query": mutation
                  },
                  headers=headers
                  )

pprint.pprint(json.loads(r.content))
