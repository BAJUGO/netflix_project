import time
from datetime import timedelta, datetime, UTC

import jwt

from fastapi import Request, Response, HTTPException

from project_dir.core import settings


def encode(data: dict, exp: timedelta, token_type: str):
    to_encode = data.copy()
    to_encode["type"] = token_type
    now = datetime.now(UTC)
    to_encode.update(exp=(now + exp), iat=now)
    token = jwt.encode(
        payload=to_encode,
        key=settings.jwt.private_key.read_text(),
        algorithm=settings.jwt.algorithm,
    )
    return token


def encode_access_token(data: dict, exp: timedelta = settings.jwt.expire_time_access):
    return encode(data, exp, "access")


def encode_refresh_token(data: dict, exp: timedelta = settings.jwt.expire_time_refresh):
    return encode(data, exp, "refresh")


def decode_token(token: str):
    return jwt.decode(
        token,
        key=settings.jwt.public_key.read_text(),
        algorithms=[settings.jwt.algorithm],
    )

def get_token_from_cookies(request: Request, token_type: str):
    try:
        token = request.cookies.get(token_type)
        decoded_token = decode_token(token)
        if decoded_token["exp"] < time.time():
            raise HTTPException(status_code=401, detail='not authenticated')
        return decoded_token
    except Exception as e:
        print(e)


def set_new_tokens(data: dict, response: Response):
    new_access_token = encode_access_token(data=data)
    new_refresh_token = encode_refresh_token(data=data)
    response.set_cookie(key="access_token", value=new_access_token, max_age=60 * 15, httponly=True, samesite="lax", path="/")
    response.set_cookie(key="refresh_token", value=new_refresh_token, max_age=60 * 60 * 24 * 7, httponly=True, samesite="lax", path="/")
    return response

