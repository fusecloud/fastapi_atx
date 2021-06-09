# todo; testing - remove later and replace with normal models?
import fastapi
from fastapi import FastAPI, Body

from data.models.chores import Chore
from data.models.apiuser import ApiUser
from api.auth.auth_handler import sign_jwt

api = fastapi.APIRouter()

users = []


@api.post("/api/auth", tags=["user"])
async def create_user(user: ApiUser = Body(...)):
    # users.append(user)  # replace with db call, making sure to hash the password first
    return sign_jwt(user.email)
