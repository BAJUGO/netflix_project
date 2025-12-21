from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import AuthorCreate, MovieCreate
from ..core import db_helper
from ..models import Author, Movie

async def add_author_session(author_in: AuthorCreate, session: AsyncSession):
    author = Author(**author_in.model_dump())
    session.add(author)
    await session.commit()
    await session.refresh(author)
    return author


async def add_movie_session(movie_in: MovieCreate, session: AsyncSession):
    movie = Movie(**movie_in.model_dump())
    session.add(movie)
    await session.commit()
    await session.refresh(movie)
    return movie