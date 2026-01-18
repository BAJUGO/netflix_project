from typing import TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, InstrumentedAttribute

import project_dir.views_part.schemas as schemas
from project_dir.models import Author, Movie, Series
from project_dir.views_part.global_crud.crud import model_to_schema, models_to_schemas

T = TypeVar("T", Movie, Series)


async def get_author_content_rel_session(session: AsyncSession, base_class_attribute: InstrumentedAttribute, schema: type[BaseModel]):
    stmt = select(Author).options(selectinload(base_class_attribute)).order_by(Author.id)
    authors = list(await session.scalars(stmt))
    result = {}
    for author in authors:
        items = getattr(author, base_class_attribute.key)
        result[f"Author {author.id} {base_class_attribute.key}"] = await models_to_schemas(items, schema) if items else ["No data"]
    return result


async def get_series_of_author_rel_session(session: AsyncSession):
    return await get_author_content_rel_session(session=session, base_class_attribute=Author.series, schema=schemas.SeriesSchema)


async def get_movies_of_author_rel_session(session: AsyncSession):
    return await get_author_content_rel_session(session=session, base_class_attribute=Author.movies, schema=schemas.MovieSchema)


async def get_author_of_content_rel_session(session: AsyncSession, base_class: type[T], base_class_author: InstrumentedAttribute, content_id: int):
    stmt = select(base_class).where(base_class.id == content_id).options(selectinload(base_class_author))
    obj = await session.scalar(stmt)
    if obj:
        return await model_to_schema(obj.author, schemas.AuthorSchema)
    raise HTTPException(status_code=404, detail=f"No such {base_class.__name__.lower()} found")


async def get_author_of_movie_rel_session(session: AsyncSession, movie_id: int):
    return await get_author_of_content_rel_session(session=session, base_class=Movie, base_class_author=Movie.author, content_id=movie_id)


async def get_author_of_series_rel_session(session: AsyncSession, series_id: int):
    return await get_author_of_content_rel_session(session=session, base_class=Series, base_class_author=Series.author, content_id=series_id)
