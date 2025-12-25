from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AuthorCreate, MovieCreate, UserCreate, SeriesCreate
from project_dir.authorization import hash_password
from project_dir.models import Author, Movie, Series, User

SCHEMAS_CLS = {
    "AUTHOR": Author,
    "MOVIE": Movie,
    "SERIES": Series,
    "USER": User
}


async def adder_session(data: BaseModel, session: AsyncSession, schema_name: str):
    cls = SCHEMAS_CLS[schema_name]
    obj = cls(**data.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def getter_session(session: AsyncSession, schema_name: str) -> list[Movie | Series | Author | User]:
    cls = SCHEMAS_CLS[schema_name]
    stmt = Select(cls).order_by(cls.id)
    result = await session.scalars(stmt)
    return list(result)


async def getter_by_id_session(session: AsyncSession, schema_name: str, obj_id: int) -> type[
    Author | Movie | User | Series]:
    cls = SCHEMAS_CLS[schema_name]
    obj = await session.get(cls, obj_id)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"{schema_name.lower()} wasn't found")
    return obj


async def deleter_session(session: AsyncSession, obj_id: int, schema_name: str) -> str:
    obj_to_del = await getter_by_id_session(session=session, schema_name=schema_name, obj_id=obj_id)
    await session.delete(obj_to_del)
    await session.commit()
    return f"{schema_name} has been deleter"


async def add_author_session(author_in: AuthorCreate, session: AsyncSession) -> Author:
    return await adder_session(author_in, session, "AUTHOR")


async def add_movie_session(movie_in: MovieCreate, session: AsyncSession) -> Movie:
    return await adder_session(movie_in, session, "MOVIE")


async def add_series_session(series_in: SeriesCreate, session: AsyncSession) -> Series:
    return await adder_session(series_in, session, "SERIES")


async def add_user_session(user_in: UserCreate, session: AsyncSession) -> str:
    user = User(**user_in.model_dump(exclude={"password"}), hashed_password=hash_password(user_in.password),
                role="user", active=True)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return f"Hello user {user.visible_name}! You have registered, and your ID is {user.id}"


async def delete_user_session(user_to_delete_id: int, session: AsyncSession):
    return await deleter_session(session=session, obj_id=user_to_delete_id, schema_name="USER")


async def delete_author_session(session: AsyncSession, author_to_delete_id: int):
    return await deleter_session(session, author_to_delete_id, "AUTHOR")


async def delete_series_session(session: AsyncSession, series_to_delete_id: int):
    return await deleter_session(session, series_to_delete_id, "SERIES")


async def get_authors_session(session: AsyncSession) -> list[Author]:
    return await getter_session(session, "AUTHOR")


async def get_movies_session(session: AsyncSession) -> list[Movie]:
    return await getter_session(session, "MOVIE")


async def get_series_session(session: AsyncSession) -> list[Series]:
    return await getter_session(session, "SERIES")


async def change_role_session(session: AsyncSession, user_id: int, new_role: str):
    user = await getter_by_id_session(session, "USER", user_id)
    user.role = new_role
    await session.commit()
    await session.refresh(user)
    return f"{user.visible_name} role has been changed to {user.role}"
