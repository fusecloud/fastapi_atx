import json
from typing import Optional, List, Dict

import fastapi
from fastapi import Header, Body, Depends
from api.models.chore import Chore
from api.models.user import User
from fastapi.openapi.models import APIKey
from starlette import status

from services import chore_service, user_service

from starlette.status import HTTP_403_FORBIDDEN
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

router = fastapi.APIRouter()

# API_KEY = "1234567asdfgh"
API_HEADER_KEY_NAME = "Authorization"
api_key_header_auth = APIKeyHeader(name=API_HEADER_KEY_NAME, auto_error=True)


# todo: abstract this to infrastructure folder
async def get_api_key(api_key_header: str = Security(api_key_header_auth)) -> User:
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
        )

    print("api_key_header")
    print(api_key_header)
    user = await user_service.get_user_by_api_key(api_key_header)
    print("user")
    print(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    return user


@router.get('/api/chores', dependencies=[Security(get_api_key)], name="all_chores", response_model=List[Chore])
async def all_chores(user: User = Depends(get_api_key)) -> Optional[List[Chore]]:
    """
    Returns all of an authorized user's chores
    """

    print("found user:....")
    print(user)

    return await chore_service.get_user_chores(user_id=user.id)

# todo: add additional docs
# get specific chore
# create a chore
# update a chore
# delete a chore

# todo: add examples in routes
