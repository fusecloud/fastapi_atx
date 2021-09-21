from typing import Optional, List, Dict
import fastapi
from fastapi import Header, Body, Depends
from api.models.chore import Chore
from api.models.user import User
from starlette import status
from starlette.responses import Response

from services import chore_service, user_service
from infrastructure.api_auth import get_api_key
from fastapi import Security, HTTPException

router = fastapi.APIRouter()


@router.get('/api/chores', dependencies=[Security(get_api_key)], name="get chores", response_model=List[Chore])
async def get_chores(search_criteria: Optional[Dict] = None,
                     user: User = Depends(get_api_key)) -> Optional[List[Chore]]:
    """
    Returns all of an authorized user's chores
    """

    if search_criteria and search_criteria['chore_id']:
        print(f"User searched for chore: {search_criteria['chore_id']}")

    return await chore_service.get_user_chores(
        user_id=user.user_id,
        chore_id=search_criteria['chore_id'] if search_criteria and search_criteria['chore_id'] else None
    )


@router.post('/api/create_chore', dependencies=[Security(get_api_key)], name="create chore")
async def create_chore(search_criteria: Chore, user: User = Depends(get_api_key)) -> Response:
    """
    Creates a user chore
    """

    await chore_service.add_chore(
        user_id=user.user_id,
        name=search_criteria.chore_name,
        category=search_criteria.category,
        type=search_criteria.type,
        alert_days=search_criteria.alert_days
    )

    return Response(content="Chore Created", status_code=200)


# edit a chore
@router.post('/api/edit_chore', dependencies=[Security(get_api_key)], name="edit chore")
async def edit_chore(search_criteria: Chore, user: User = Depends(get_api_key)) -> Response:
    """
    Edits a user chore
    """

    if not search_criteria.chore_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing chore id",
        )

    await chore_service.edit_chore(
        user_id=user.user_id,
        id=search_criteria.chore_id,
        name=search_criteria.chore_name,
        category=search_criteria.category,
        type=search_criteria.type,
        alert_days=search_criteria.alert_days
    )

    return Response(content="Chore Updated", status_code=200)


# delete a chore
@router.post('/api/delete_chore', dependencies=[Security(get_api_key)], name="delete chore")
async def delete_chore(search_criteria: Chore, user: User = Depends(get_api_key)) -> Response:
    """
    Deletes a user chore
    """
    if not search_criteria.chore_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing chore id",
        )

    await chore_service.remove_chore(
        user_id=user.user_id,
        id=search_criteria.chore_id,
    )

    return Response(content="Chore Deleted", status_code=200)

# todo: add examples in routes
# https://fastapi.tiangolo.com/tutorial/schema-extra-example/