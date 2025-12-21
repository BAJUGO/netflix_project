from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from project_dir.core.db_helper import db_helper

from project_dir.views_part.crud import add_author_session, add_movie_session
from project_dir.views_part.schemas import AuthorCreate, AuthorSchema, MovieSchema, MovieCreate

router = APIRouter()


@router.post("/add_author", response_model=AuthorSchema)
async def add_author(author_in: AuthorCreate, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await add_author_session(author_in, session)


@router.post("/add_movie", response_model=MovieSchema)
async def add_movie(movie_in: MovieCreate, session: AsyncSession = Depends(db_helper.session_dependency)):
    return await add_movie_session(movie_in, session)
