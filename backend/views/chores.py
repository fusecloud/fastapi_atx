import asyncio

import fastapi_chameleon
from fastapi_chameleon import template
import fastapi
from starlette import status
from starlette.requests import Request

from viewmodels.account.account_view_model import AccountViewModel
from viewmodels.chores.chore_view_model import ChoreViewModel
from viewmodels.account.login_view_model import LoginViewModel
from viewmodels.account.register_view_model import RegisterViewModel
from infrastructure import cookie_auth
from services import user_service, chore_service

router = fastapi.APIRouter()

fastapi_chameleon.global_init('templates')


# get
@router.get('/chores')
@template(template_file='chores/index.pt')
async def index(request: Request):
    vm = ChoreViewModel(request)

    if not vm.user_id:
        response = fastapi.responses.RedirectResponse(url="/account/login", status_code=status.HTTP_302_FOUND)
        return response

    await vm.load()
    return vm.to_dict()


# get specific chore
@router.get('/chores/{id}')
@template(template_file='chores/selected.pt')
async def index_selected(request: Request, id: int):
    vm = ChoreViewModel(request)

    if not vm.user_id:
        response = fastapi.responses.RedirectResponse(url="/account/login", status_code=status.HTTP_302_FOUND)
        return response

    await vm.load(chore_id=id)
    return vm.to_dict()


# create a chore form the form
@router.get('/create_chore')
@template(template_file='chores/create.pt')
async def index(request: Request):
    vm = ChoreViewModel(request)

    if not vm.user_id:
        response = fastapi.responses.RedirectResponse(url="/account/login", status_code=status.HTTP_302_FOUND)
        return response

    return vm.to_dict()


@router.post('/create_chore')
@template(template_file='chores/create.pt')
async def index(request: Request):
    vm = ChoreViewModel(request)

    if not vm.user_id:
        response = fastapi.responses.RedirectResponse(url="/account/login", status_code=status.HTTP_302_FOUND)
        return response

    await vm.add_chore()
    if vm.error:
        return vm.to_dict()

    chore = \
        await chore_service.add_chore(
            user_id=vm.user_id,
            name=vm.name,
            category=vm.category,
            type=vm.type,
            alert_days=vm.alert_days
        )

    response = fastapi.responses.RedirectResponse(url=f"/chores/{chore.id}", status_code=status.HTTP_302_FOUND)
    return response


# delete a chore
@router.post('/chores/{id}/delete')
async def index(request: Request, id: int):
    vm = ChoreViewModel(request)

    if not vm.user_id:
        response = fastapi.responses.RedirectResponse(url="/account/login", status_code=status.HTTP_302_FOUND)
        return response

    await chore_service.remove_chore(id=id, user_id=vm.user_id)
    response = fastapi.responses.RedirectResponse(url=f"/chores", status_code=status.HTTP_302_FOUND)

    return response


# edit
@router.get('/chores/{id}/edit')
@template(template_file='chores/edit.pt')
async def index(request: Request, id: int):
    vm = ChoreViewModel(request)

    if not vm.user_id:
        response = fastapi.responses.RedirectResponse(url="/account/login", status_code=status.HTTP_302_FOUND)
        return response

    await vm.load(chore_id=id)
    return vm.to_dict()


@router.post('/chores/{id}/edit')
@template(template_file='chores/edit.pt')
async def index(request: Request, id: int):
    vm = ChoreViewModel(request)

    if not vm.user_id:
        response = fastapi.responses.RedirectResponse(url="/account/login", status_code=status.HTTP_302_FOUND)
        return response

    await vm.add_chore()
    if vm.error:
        return vm.to_dict()

    await chore_service.edit_chore(
        id=id,
        user_id=vm.user_id,
        name=vm.name,
        category=vm.category,
        type=vm.type,
        alert_days=vm.alert_days
    )

    response = fastapi.responses.RedirectResponse(url=f"/chores/{id}", status_code=status.HTTP_302_FOUND)
    return response
