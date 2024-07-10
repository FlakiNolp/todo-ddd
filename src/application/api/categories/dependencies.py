from typing import Annotated

from joserfc import jwt
from fastapi import Cookie
from joserfc.jwt import Token


def user_auth(access_token: Annotated[str, Cookie(alias="access-token")]) -> Token:
    try:
        return jwt.decode(access_token, key="ok", algorithms=["HS256"])
    except:
        raise
