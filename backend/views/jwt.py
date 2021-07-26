from datetime import timedelta

import asyncio
import fastapi_chameleon
import fastapi
from fastapi_chameleon import template

from services import user_service
from data.models.user import User

from infrastructure.jwt import create_access_token
from infrastructure import cookie_auth
from infrastructure.cookie_auth import set_jwt

from viewmodels.account.jwt_login_view_model import JwtLoginViewModel
from viewmodels.account.jwt_restricted_view_model import JwtRestrictedViewModel

from fastapi import Depends, HTTPException, status
from starlette.requests import Request

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = fastapi.APIRouter()

fastapi_chameleon.global_init('templates')


@router.get('/account/jwt_login')
@template(template_file='account/jwt_login.pt')
def login_get(request: Request):
    vm = JwtLoginViewModel(request)
    # normal login check
    if not vm.user_id:
        response = fastapi.responses.RedirectResponse(url="/account/login", status_code=status.HTTP_302_FOUND)
        return response
    return vm.to_dict()


@router.post("/account/jwt_login")
@template(template_file='account/jwt_login.pt')
async def login_post(request: Request):
    vm = JwtLoginViewModel(request)

    await vm.load()
    if vm.error:
        return vm.to_dict()

    user = await user_service.login_user(vm.email, vm.password)

    if not user:
        await asyncio.sleep(3)
        vm.error = "The account does not exist or the password is wrong."
        return vm.to_dict()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        # The JWT specification says that there's a key sub, with the subject of the token.
        # It's optional to use it, but that's where you would put the user's identification, so we are using it here

        # to avoid ID collisions, when creating the JWT token for the user, you could prefix the value of the sub key,
        # e.g. with username:. So, in this example, the value of sub could have been: username:johndoe
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    # jwt_object = {"access_token": access_token, "token_type": "bearer"}
    resp = fastapi.responses.RedirectResponse('/account/jwt_restricted', status_code=status.HTTP_302_FOUND)
    set_jwt(resp, jwt_object=access_token)
    return resp


@router.get("/account/jwt_restricted/")
@template(template_file='account/jwt_restricted.pt')
async def index(request: Request):
    vm = JwtRestrictedViewModel(request)
    # normal login check
    await vm.load()
    if not vm.user_id:
        response = fastapi.responses.RedirectResponse(url="/account/login", status_code=status.HTTP_302_FOUND)
        return response

    if not vm.jwt_user_id:
        response = fastapi.responses.RedirectResponse(url="/account/jwt_login", status_code=status.HTTP_302_FOUND)
        return response

    return vm.to_dict()


@router.get('/account/jwt/logout')
def logout(request: Request):
    response = fastapi.responses.RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    cookie_auth.logout_jwt(response)

    return response
