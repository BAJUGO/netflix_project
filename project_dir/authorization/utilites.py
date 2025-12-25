import bcrypt

from fastapi import Depends, Form, HTTPException
from pydantic import EmailStr
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from project_dir.core import db_helper
from project_dir.models import User


def hash_password(plain_pw: str):
    plain_byted_pw = plain_pw.encode()
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(plain_byted_pw, salt)
    return hashed_pw


def verify_password(plain_pw: str, hashed_pw: bytes):
    plain_byted_pw = plain_pw.encode()
    return bcrypt.checkpw(password=plain_byted_pw, hashed_password=hashed_pw)


# ! Здесь написали,что принимаем username просто чтобы oauth2_schema не жаловалась, ведь она ожидает принятия username и password
# ! Эта функция - форма дял create_token. Oauth2_schema использует свою форму (username, password), поэтому здесь формы должны быть
# ! Одинаковыми
async def authenticate_user(session: AsyncSession = Depends(db_helper.session_dependency), username: str = Form(...),
                            password: str = Form(...)):
    stmt = Select(User).where(User.email == username)
    user = await session.scalar(stmt)
    if user is None:
        raise HTTPException(status_code=401, detail="email is incorrect")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="password is incorrect")
    return user

# async def do_stuf():
#     async with db_helper.session_factory() as session:
#         user = User(
#             visible_name="test 1",
#             username="dima",
#             hashed_password=hash_password("kiril12AZ"),
#             role="user",
#             active=True,
#         )
#         session.add(user)
#         await session.commit()
#         await session.refresh(user)
#
#
# import asyncio
#
# asyncio.run(do_stuf())
