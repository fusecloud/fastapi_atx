import asyncio

import fastapi_chameleon
from fastapi_chameleon import template
import fastapi
from starlette import status
from starlette.requests import Request

from viewmodels.account.account_view_model import AccountViewModel
from viewmodels.account.login_view_model import LoginViewModel
from viewmodels.account.register_view_model import RegisterViewModel
from infrastructure import cookie_auth
from services import user_service

router = fastapi.APIRouter()

fastapi_chameleon.global_init('templates')


@router.get('/account', include_in_schema=False)
@template()
async def index(request: Request):
    vm = AccountViewModel(request)
    await vm.load()
    return vm.to_dict()


# ################### REGISTER #################################
@router.get('/account/register', include_in_schema=False)
@template()
def register(request: Request):
    """
    Create the form
    :param request:
    :return:
    """
    print("GET REGISTER")
    vm = RegisterViewModel(request)
    return vm.to_dict()


@router.post('/account/register', include_in_schema=False)
@template()
async def register(request: Request):
    """
    Greet user & send on way
    :param request:
    :return:
    """
    print("POST REGISTER")
    vm = RegisterViewModel(request)

    # this is needed for parsing of the form (validation in register viewmodel)
    await vm.load()
    if vm.error:
        return vm.to_dict()

    account = await user_service.create_account(vm.name, vm.email, vm.password)

    # login user
    response = fastapi.responses.RedirectResponse(url="/account", status_code=status.HTTP_302_FOUND)
    cookie_auth.set_auth(response, account.id)

    return response


# ################### LOGIN/LOGOUT #################################
@router.get('/account/login', include_in_schema=False)
@template(template_file='account/login.pt')
def login_get(request: Request):
    vm = LoginViewModel(request)
    return vm.to_dict()


@router.post('/account/login', include_in_schema=False)
@template(template_file='account/login.pt')
async def login_post(request: Request):
    vm = LoginViewModel(request)
    await vm.load()

    if vm.error:
        return vm.to_dict()

    user = await user_service.login_user(vm.email, vm.password)
    if not user:
        # can add this to add expense to people trying to hack site
        # by guessing passwords
        # if people are constantly trying to guess passwords,
        # WHY? the crypto unhash part in user_service.login_user can get sort of expensive
        await asyncio.sleep(3)
        vm.error = "The account does not exist or the password is wrong."
        return vm.to_dict()

    resp = fastapi.responses.RedirectResponse('/account', status_code=status.HTTP_302_FOUND)
    cookie_auth.set_auth(resp, user.id)

    return resp


@router.get('/account/logout', include_in_schema=False)
def logout(request: Request):
    response = fastapi.responses.RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    cookie_auth.logout(response)

    return response


