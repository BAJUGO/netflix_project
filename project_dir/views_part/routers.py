from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project_dir.authorization import oauth2_schema, get_current_user_access_token, admin_dep, admin_or_mod_dep
from project_dir.core import db_helper

from project_dir.views_part.crud import (
    add_author_session,
    add_movie_session,
    get_authors_session,
    get_movies_session,
    delete_author_session,
    add_user_session,
    add_series_session,
    get_series_session
)
from project_dir.views_part.schemas import (
    AuthorCreate,
    AuthorSchema,
    MovieSchema,
    MovieCreate,
    UserCreate,
    SeriesCreate,
    SeriesSchema
)

router = APIRouter(dependencies=[Depends(get_current_user_access_token)], tags=["contents"])

ses_dep = Depends(db_helper.session_dependency)  # type = AsyncSession


@router.post("/authors/add_author", response_model=AuthorSchema)
async def add_author(author_in: AuthorCreate, session: AsyncSession = ses_dep, adm_or_mod=admin_or_mod_dep):
    return await add_author_session(author_in, session)


@router.post("/movies/add_movie", response_model=MovieSchema)
async def add_movie(movie_in: MovieCreate, session: AsyncSession = ses_dep, adm_or_mod=admin_or_mod_dep):
    return await add_movie_session(movie_in, session)


@router.post("/series/add_series", response_model=SeriesSchema)
async def add_series(series_in: SeriesCreate, session: AsyncSession = ses_dep, adm_or_mod=admin_or_mod_dep):
    return await add_series_session(series_in, session)


@router.get("/movies/authors/get_authors", response_model=list[AuthorSchema])
async def get_authors(session: AsyncSession = ses_dep):
    return await get_authors_session(session)


@router.get("/movies/get_movies", response_model=list[MovieSchema])
async def get_movies(session: AsyncSession = ses_dep):
    return await get_movies_session(session)


@router.get("/series/get_series", response_model=list[SeriesSchema])
async def get_series(session: AsyncSession = ses_dep):
    return await get_series_session(session)


@router.delete("/authors/{author_id}")
async def delete_author(author_id: int, session: AsyncSession = ses_dep, adm_or_mod=admin_or_mod_dep):
    return await delete_author_session(session, author_id)
