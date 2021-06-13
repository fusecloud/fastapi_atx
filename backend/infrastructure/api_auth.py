from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status

from api.models.user import User
from services import user_service

API_HEADER_KEY_NAME = "Authorization"
api_key_header_auth = APIKeyHeader(name=API_HEADER_KEY_NAME, auto_error=True)


async def get_api_key(api_key_header: str = Security(api_key_header_auth)) -> User:
    if not api_key_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
        )

    user = await user_service.get_user_by_api_key(api_key_header)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    return user
