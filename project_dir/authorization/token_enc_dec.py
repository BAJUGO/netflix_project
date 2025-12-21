from datetime import timedelta, datetime, UTC

import jwt

from project_dir.core import settings


def encode_access_token(data: dict, exp: timedelta = settings.jwt.expire_time_minutes):
    to_encode = data.copy()
    now = datetime.now(UTC)
    to_encode.update(exp=(now + exp), iat=now)
    token = jwt.encode(payload=to_encode, key=settings.jwt.private_key.read_text(), algorithm=settings.jwt.algorithm)
    return token



def decode_access_token(token: str):
    return jwt.decode(token, key=settings.jwt.public_key.read_text(), algorithms=[settings.jwt.algorithm])

