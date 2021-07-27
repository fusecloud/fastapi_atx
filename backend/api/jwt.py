from datetime import timedelta

from fastapi import Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import fastapi
from fastapi import Header, Body, Depends, status

from api.models.user import User

from services import chore_service, user_service
from infrastructure.api_auth import get_api_key, get_user_creds, \
    get_user_email_str, get_user_id_via_jwt_token, get_access_token, \
    get_refresh_token, validate_refresh_token

from infrastructure.jwt import create_access_token

router = fastapi.APIRouter()
security = HTTPBearer()

# minutes until expiration
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 30


@router.post('/api/jwt_login')
async def login(user: User = Depends(get_user_creds)):
    # refresh token
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_access_token(
        data={"sub": user.email, 'scope': 'refresh'}, expires_delta=refresh_token_expires
    )

    # access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, 'scope': 'access'}, expires_delta=access_token_expires
    )

    return {
        "refresh_token": refresh_token,
        "access_token": access_token
    }


# refresh token endpoint, provides a new access token
@router.get('/api/refresh_token')
async def refresh_token(email: str = Depends(validate_refresh_token)):
    print("Refresh token passed:")
    print(refresh_token)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": email, 'scope': 'access'}, expires_delta=access_token_expires
    )

    return {"access_token": access_token}


# protected endpoint
@router.get('/api/secret')
async def secret(access_token: str = Depends(get_access_token)):
    print("Access token passed:")
    print(access_token)
    user = await get_user_id_via_jwt_token(access_token)
    if not user:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Access Token for User, Try Refreshing",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception
    return {"secret_user_id": user, "message": "This information is protected"}
