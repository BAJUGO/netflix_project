from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AuthorCreate, MovieCreate
from ..models import Author, Movie, Series

SCHEMAS_CLS = {
    "AUTHOR": Author,
    "MOVIE": Movie,
    "SERIES": Series
}


async def adder_session(data: BaseModel, session: AsyncSession, schema: str):
    cls = SCHEMAS_CLS[schema]
    obj = cls(**data.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def getter_session(session: AsyncSession, schema_name: str):
    cls = SCHEMAS_CLS[schema_name]
    stmt = Select(cls).order_by(cls.id)
    result = await session.scalars(stmt)
    return list(result)


async def deleter_session(session: AsyncSession, obj_id: int, schema_name: str, ):
    cls = SCHEMAS_CLS[schema_name]
    obj_to_del = await session.get(cls, obj_id)
    if obj_to_del is None:
        raise HTTPException(status_code=404, detail=f"{schema_name.lower()} wasn't found")
    await session.delete(obj_to_del)
    await session.commit()
    return {f"{schema_name} has been deleter"}


async def delete_author_session(session: AsyncSession, obj_id: int):
    return await deleter_session(session, obj_id, "AUTHOR")


async def add_author_session(author_in: AuthorCreate, session: AsyncSession) -> Author:
    return await adder_session(author_in, session, "AUTHOR")


async def add_movie_session(movie_in: MovieCreate, session: AsyncSession) -> Movie:
    return await adder_session(movie_in, session, "MOVIE")


async def get_authors_session(session: AsyncSession) -> list[Author]:
    return await getter_session(session, "AUTHOR")


async def get_movies_session(session: AsyncSession) -> list[Movie]:
    return await getter_session(session, "MOVIE")


async def get_series_session(session: AsyncSession) -> list[Series]:
    return await getter_session(session, "SERIES")
