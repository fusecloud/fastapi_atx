import time
from typing import Dict

import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


# A JWT is not encrypted. It's based64 encoded and signed.
# So anyone can decode the token and use its data.
# But only the server can verify it's authenticity using the JWT_SECRET

def token_response(token: str):
    return {
        "access_token": token
    }


def sign_jwt(user_id: str) -> Dict[str, str]:
    """
    Created a token string with payload (user_id), the secret, and the algorithm type and then return it
    :param user_id: payload
    :return: token string
    """
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600  # expiration time after gen
    }
    # token string
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decode_jwt(token: str) -> dict:
    """

    :param token: token to be decoded
    :return: decoded token if expiration time is valid, otherwise nothing
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
