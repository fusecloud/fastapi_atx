# from starlette.status import HTTP_403_FORBIDDEN
# from fastapi import Security, HTTPException
# from fastapi.security import APIKeyHeader
#
# API_KEY_NAME = "access_token"
# _api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
#
#
# async def get_api_key(api_key_header: str = Security(_api_key_header)):
#
#
# #     api_key_header == API_KEY:
# #     return api_key_header
# # # elif api_key_cookie == API_KEY:
# # #     return api_key_cookie
# # else:
# # raise HTTPException(
# #     status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
# # )
