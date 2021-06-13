import json
from typing import Optional, List, Dict

import fastapi
from fastapi import Header, Body, Depends
from api.models.chore import Chore
from api.models.user import User
from fastapi.openapi.models import APIKey
from starlette import status

from services import chore_service, user_service
from infrastructure.api_auth import get_api_key

from starlette.status import HTTP_403_FORBIDDEN
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

router = fastapi.APIRouter()


@router.get('/api/chores', dependencies=[Security(get_api_key)], name="all_chores", response_model=List[Chore])
async def all_chores(user: User = Depends(get_api_key)) -> Optional[List[Chore]]:
    """
    Returns all of an authorized user's chores
    """

    return await chore_service.get_user_chores(user_id=user.id)


@router.get('/api/chores/{id}', dependencies=[Security(get_api_key)], name="specific_chore", response_model=List[Chore])
async def all_chores(id: int, user: User = Depends(get_api_key)) -> Optional[List[Chore]]:
    """
    Returns all of an authorized user's chores
    """

    print("found user:....")
    print(user)

    return await chore_service.get_user_chores(user_id=user.id, chore_id=id)

# todo: add additional docs
# get specific chore
# create a chore
# update a chore
# delete a chore

# todo: add examples in routes
