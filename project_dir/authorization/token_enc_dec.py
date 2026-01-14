from datetime import timedelta, datetime, UTC

import jwt

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


def decode_access_token(token: str):
    return jwt.decode(
        token,
        key=settings.jwt.public_key.read_text(),
        algorithms=[settings.jwt.algorithm],
    )

