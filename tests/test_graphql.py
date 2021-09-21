import json
import pprint
import requests

# pwd="9Qmrn6amB"
api_key = "testtesttest"
headers = {
    "Authorization": api_key,
    "Content-Type": "application/json"
}

# QUERIES

# hello world
# query = \
#     """
#     {
#       hello {
#         "world
#       }
#     }
#     """
#
# r = requests.post("http://127.0.0.1:8000/graphql",
#                   json={
#                       "query": query
#                   },
#                   headers=headers
#                   )
#
# pprint.pprint(json.loads(r.content))

# Get user and/or chore data
query = \
    '''
    {
      user_chores {
        user_name
        chore_id
        chore_name
        type
        alert_days
      }
    }
    '''

# get all chores
r = requests.post("http://127.0.0.1:8000/graphql",
                  json={
                      "query": query
                  },
                  headers=headers
                  )

pprint.pprint(json.loads(r.content))

# MUTATIONS
# Add a chore
# -- needs dbl quotes
mutation = \
    '''
    mutation {
        create_chore(
            chore_name: "TEST GraphQL"
            category: "Dev"
            type: "one-time"
            alert_days: 1
        ){
            user_id
            chore_name
            category
            type
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

# Edit a chore
mutation = \
    '''
    mutation {
        edit_chore(
            chore_id: 1
            chore_name: "TEST GraphQL-UPDATED2"
            category: "Dev-UPDATED"
            type: "one-time-UPDATED"
            alert_days: 99
        ){
            chore_name
            category
            type
            alert_days
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
