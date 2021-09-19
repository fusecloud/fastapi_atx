import hashlib
from typing import Optional

from fastapi import HTTPException, status
from jose import JWTError, jwt
from starlette.requests import Request
from starlette.responses import Response

from services import user_service
from infrastructure.num_convert import try_int

# JUWT
SECRET_KEY = "50e7eda291939113a3cdf0163040d651b370d148eee62236edfe418bb8375130"
ALGORITHM = "HS256"

# COOKIES
auth_cookie_name = 'chores_account'
jwt_cookie_name = 'chores_account_jwt'


def set_auth(response: Response, user_id: int):
    hash_val = __hash_text(str(user_id))
    val = "{}:{}".format(user_id, hash_val)
    response.set_cookie(auth_cookie_name, val, secure=False, httponly=True, samesite='Lax')


def set_jwt(response: Response, jwt_object: dict):
    # hash_val = __hash_text(str(user_id))
    # val = "{}:{}".format(user_id, hash_val)
    response.set_cookie(jwt_cookie_name, jwt_object, secure=False, httponly=True, samesite='Lax')


def __hash_text(text: str) -> str:
    text = "salty__" + text + "__text"
    return hashlib.sha512(text.encode('utf-8')).hexdigest()


def get_user_id_via_auth_cookie(request: Request) -> Optional[int]:
    if auth_cookie_name not in request.cookies:
        return None

    val = request.cookies[auth_cookie_name]
    parts = val.split(":")
    if len(parts) != 2:
        return None

    user_id = parts[0]
    hash_val = parts[1]
    hash_val_check = __hash_text(user_id)
    if hash_val != hash_val_check:
        print("Warning: Hash mismatch, invalid cookie value")
        return None

    return try_int(user_id)


async def get_user_id_via_jwt_cookie(request: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if jwt_cookie_name not in request.cookies:
        return None

    token = request.cookies[jwt_cookie_name]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
        # token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    user = await user_service.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user.user_id


def logout(response: Response):
    response.delete_cookie(auth_cookie_name)


def logout_jwt(response: Response):
    response.delete_cookie(jwt_cookie_name)
