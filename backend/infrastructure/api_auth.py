from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from starlette import status

from api.models.user import User
from services import user_service

# JWT
SECRET_KEY = "50e7eda291939113a3cdf0163040d651b370d148eee62236edfe418bb8375130"
ALGORITHM = "HS256"

# API HEADERS
API_HEADER_KEY_NAME = "Authorization"
api_key_header_auth = APIKeyHeader(name=API_HEADER_KEY_NAME, auto_error=True)

EM_HEADER_NAME = "email"
em_header_auth = APIKeyHeader(name=EM_HEADER_NAME, auto_error=True)

PWD_HEADER_NAME = "pwd"
pwd_header_auth = APIKeyHeader(name=PWD_HEADER_NAME, auto_error=True)

ACCESS_TOKEN_HEADER_NAME = "access_token"
access_token_header_auth = APIKeyHeader(name=ACCESS_TOKEN_HEADER_NAME, auto_error=True)

REFRESH_TOKEN_HEADER_NAME = "refresh_token"
refresh_token_header_auth = APIKeyHeader(name=REFRESH_TOKEN_HEADER_NAME, auto_error=True)


# checks if api key token in api headers
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


# checks if email/pwd in headers and validates belong to user
async def get_user_creds(email: str = Security(em_header_auth), password: str = Security(pwd_header_auth)) -> User:
    # explicitly looks for headers we outlines above (email & password)
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Email or Password in Header",
        )

    # 2 api calls here so that we don't confirm to requester that email exists
    # could be combined into 1 and return 'Invalid Email or Password'
    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Email",
        )
    user_validated = await user_service.login_user(email, password)
    if not user_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Password",
        )

    return user


# checks if access token in api headers
async def get_access_token(access_token: str = Security(access_token_header_auth)):
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Access Token in Header",
        )
    return access_token


# checks if refresh token in api headers
async def get_refresh_token(refresh_token: str = Security(refresh_token_header_auth)):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Refresh Token in Header",
        )
    return refresh_token


# checks if email in api headers
async def get_user_email_str(email: str = Security(em_header_auth)):
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Email in Header",
        )


# validates refresh token and, if valid, issues new access token
async def validate_refresh_token(refresh_token: str = Security(refresh_token_header_auth)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials, Try Logging in Again",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        scope: str = payload.get("scope")

        if email is None or scope != 'refresh':
            raise credentials_exception
        # token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    return email


# for example, pulls userid from email on the access token after decoding
async def get_user_id_via_jwt_token(access_token: str = Security(access_token_header_auth)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
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
