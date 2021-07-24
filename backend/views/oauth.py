from datetime import timedelta

import fastapi_chameleon
import fastapi
from data.models.oauth import User, UserInDB, Token, TokenData
from fastapi_chameleon import template
from infrastructure.oauth import get_current_user, fake_users_db, fake_hash_password, \
    authenticate_user, create_access_token, get_current_active_user

from data.models.user import User
from services import user_service
from viewmodels.account.oauth_login_view_model import OauthLoginViewModel

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.requests import Request

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = fastapi.APIRouter()

fastapi_chameleon.global_init('templates')

# Oauth2 + password flow + bearer
# https://fastapi.tiangolo.com/tutorial/security/first-steps/

# When we create an instance of the OAuth2PasswordBearer class
# we pass in the tokenUrl parameter.
# This parameter contains the URL that the client
# (the frontend running in the user's browser) will use to
# send the username and password in order to get a token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Because we are using a relative URL, if your API was located at
# https://example.com/, then it would refer to https://example.com/token.
#
# But if your API was located at https://example.com/api/v1/,
# then it would refer to https://example.com/api/v1/token
# Using a relative URL is important to make sure your application
# keeps working even in an advanced use case like Behind a Proxy.
# https://fastapi.tiangolo.com/advanced/behind-a-proxy/

# The oauth2_scheme variable is an instance of OAuth2PasswordBearer, but it is also a "callable".
# It could be called as:
# oauth2_scheme(some, parameters)
# So, it can be used with Depends.

# This dependency will provide a str that is assigned to the parameter token of the path operation function.
# FastAPI will know that it can use this dependency to define a "security scheme" in the OpenAPI schema (and the automatic API docs).


@router.get('/account/oauth')
async def read_items(token: str = Depends(oauth2_scheme)):
    """
    It will go and look in the request for that Authorization header, check if the value is Bearer plus some token, and will return the token as a str.

    If it doesn't see an Authorization header, or the value doesn't have a Bearer token, it will respond with a 401 status code error (UNAUTHORIZED) directly.
    :param token:
    :return:
    """
    return {"token": token}


# @router.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     return {"access_token": user.username, "token_type": "bearer"}


# @router.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user

# @router.post("/token", response_model=Token)
# # todo: swap this out for a html form
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         # The JWT specification says that there's a key sub, with the subject of the token.
#         # It's optional to use it, but that's where you would put the user's identification, so we are using it here
#
#         # to avoid ID collisions, when creating the JWT token for the user, you could prefix the value of the sub key,
#         # e.g. with username:. So, in this example, the value of sub could have been: username:johndoe
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
@router.get('/account/oauth_login')
@template(template_file='account/oauth_login.pt')
def login_get(request: Request):
    vm = OauthLoginViewModel(request)
    return vm.to_dict()


@router.post("/account/oauth_login", response_model=Token)
@template(template_file='account/oauth_login.pt')
async def login_for_access_token(request: Request):
    vm = OauthLoginViewModel(request)

    if not vm.user_id:
        response = fastapi.responses.RedirectResponse(url="/account/login", status_code=status.HTTP_302_FOUND)
        return response

    await vm.login()
    if vm.error:
        return vm.to_dict()

    # user = authenticate_user(fake_users_db, form_data.username, form_data.password)

    user = await user_service.login_user(vm.email, vm.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        # The JWT specification says that there's a key sub, with the subject of the token.
        # It's optional to use it, but that's where you would put the user's identification, so we are using it here

        # to avoid ID collisions, when creating the JWT token for the user, you could prefix the value of the sub key,
        # e.g. with username:. So, in this example, the value of sub could have been: username:johndoe
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
#
#
# @router.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]
