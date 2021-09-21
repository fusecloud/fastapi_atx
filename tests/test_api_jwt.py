import json
import pprint
import requests
from datetime import datetime

# 1: LOGIN
email = "test@test.com"
pwd = "testtesttest"
# create header with uid/pass
headers = {"email": email, "pwd": pwd}
# login to get access token & refresh token
r1 = requests.post("http://127.0.0.1:8000/api/jwt_login",
                   headers=headers)
r_dict1 = json.loads(r1.content)
pprint.pprint(r_dict1)

# 2: ACCESS TOKEN: POSITIVE TEST
# get the access token from the response & pass it to next call's header
# can use this until it expires
headers = {"access_token": r_dict1.get('access_token')}

r2 = requests.get("http://127.0.0.1:8000/api/secret",
                  headers=headers)
r_dict2 = json.loads(r2.content)
pprint.pprint(r_dict2)

# 3: ACCESS TOKEN: NEGATIVE TEST
# try with a 'wrong' access token
bad_access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1ZXN0QHRlc3QuY29tIiwic2NvcGUiOiJhY2Nlc3MiLCJleHAiOjE2Mjc0MTQ1Mzd9._hNOSEIZvlM_E2RS-O5ziKa5km-ElTgMZ0CMMAoxy8N'
headers = {"access_token": bad_access_token}

r3 = requests.get("http://127.0.0.1:8000/api/secret",
                  headers=headers)
r_dict3 = json.loads(r3.content)
pprint.pprint(r_dict3)

# 4: REFRESH TOKEN: POSITIVE TEST
headers = {"refresh_token": r_dict1.get('refresh_token')}

r4 = requests.get("http://127.0.0.1:8000/api/refresh_token",
                  headers=headers)
r_dict4 = json.loads(r4.content)
pprint.pprint(r_dict4)

# pprint.pprint(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# 5: REFRESH TOKEN: NEGATIVE TEST
headers = {"refresh_token": bad_access_token}

r4 = requests.get("http://127.0.0.1:8000/api/refresh_token",
                  headers=headers)
r_dict4 = json.loads(r4.content)
pprint.pprint(r_dict4)

# pprint.pprint(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
