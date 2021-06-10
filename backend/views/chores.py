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
@router.get('/chores', include_in_schema=True)
@template(template_file='chores/index.pt')
async def index(request: Request):
    vm = ChoreViewModel(request)
    await vm.load()
    return vm.to_dict()


# get specific chore
@router.get('/chores/{id}', include_in_schema=True)
@template(template_file='chores/selected.pt')
async def index_selected(request: Request, id: int):
    vm = ChoreViewModel(request)
    await vm.load(chore_id=id)
    print("RESULT")
    print(vm.to_dict())
    return vm.to_dict()


# CREATE CHORE FORM
@router.get('/create_chore', include_in_schema=True)
@template(template_file='chores/create.pt')
async def index(request: Request):
    vm = ChoreViewModel(request)
    # await vm.add_new_chore()
    return vm.to_dict()


@router.post('/create_chore', include_in_schema=True)
@template(template_file='chores/create.pt')
async def index(request: Request):
    vm = ChoreViewModel(request)
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


# put

# delete/edit intent
@router.post('/chores/{id}={action}', include_in_schema=True)
async def index(id: int, action: str):
    print(action)
    if action == 'delete':
        print(action)
        await chore_service.remove_chore(id=id)

        response = fastapi.responses.RedirectResponse(url=f"/chores", status_code=status.HTTP_302_FOUND)

        return response

    elif action == 'edit':
        response = fastapi.responses.RedirectResponse(url=f"/chores/{id}/edit", status_code=status.HTTP_302_FOUND)

        return response


# edit
@router.get('/chores/{id}/edit', include_in_schema=True)
@template(template_file='chores/edit.pt')
async def index(request: Request, id: int):
    vm = ChoreViewModel(request)
    await vm.load(chore_id=id)
    return vm.to_dict()


@router.post('/chores/{id}/edit', include_in_schema=True)
@template(template_file='chores/edit.pt')
async def index(request: Request, id: int):
    vm = ChoreViewModel(request)
    await vm.add_chore()
    if vm.error:
        return vm.to_dict()

    await chore_service.edit_chore(
        id=id,
        name=vm.name,
        category=vm.category,
        type=vm.type,
        alert_days=vm.alert_days
    )

    response = fastapi.responses.RedirectResponse(url=f"/chores/{id}", status_code=status.HTTP_302_FOUND)
    return response
