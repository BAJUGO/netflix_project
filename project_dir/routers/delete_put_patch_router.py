from fastapi import Form, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from project_dir.authorization import admin_or_mod_dep, admin_dep
from project_dir.core import ses_dep


import project_dir.views_part.crud as crud
import project_dir.views_part.schemas as schemas


router = APIRouter()

@router.delete("/authors/{author_id}", dependencies=[admin_or_mod_dep], tags=["author", "delete"])
async def delete_author(author_id: int, session: AsyncSession = ses_dep):
    return await crud.delete_author_session(session, author_id)


@router.delete("/series/{series_id}", dependencies=[admin_or_mod_dep], tags=["movie", "delete"])
async def delete_series(series_id: int, session: AsyncSession = ses_dep):
    return await crud.delete_series_session(session, series_id)


@router.delete("/movies/{movie_id}", response_model=schemas.MovieSchema, dependencies=[admin_or_mod_dep],
               tags=["series", "delete"])
async def delete_movie(movie_id: int, session: AsyncSession = ses_dep):
    return await crud.delete_movie_session(session, movie_id)


@router.delete("/delete_account", tags=["user", "delete"], dependencies=[admin_dep])
async def delete_user(user_id: int, session: AsyncSession = ses_dep):
    return await crud.delete_user_session(user_to_delete_id=user_id, session=session)


@router.put("/authors/{author_id}", response_model=schemas.AuthorSchema, dependencies=[admin_or_mod_dep],
            tags=["author", "update"])
async def update_author(author_id: int, author_schema: schemas.AuthorCreate, session: AsyncSession = ses_dep):
    return await crud.full_update_author_session(session, author_id, author_schema)


@router.put("/movies/{movie_id}", response_model=schemas.MovieSchema, dependencies=[admin_or_mod_dep],
            tags=["movie", "update"])
async def full_update_movie(movie_id: int, movie_schema: schemas.MovieCreate, session: AsyncSession = ses_dep):
    return await crud.full_update_movie_session(session, movie_id, movie_schema)


@router.put("/series/{series_id}", response_model=schemas.SeriesSchema, dependencies=[admin_or_mod_dep],
            tags=["series", "update"])
async def full_update_series(series_id: int, series_schema: schemas.SeriesCreate, session: AsyncSession = ses_dep):
    return await crud.full_update_series_session(session, series_id, series_schema)


@router.patch("/authors/{author_id}", response_model=schemas.AuthorSchema, dependencies=[admin_or_mod_dep],
              tags=["author", "update"])
async def update_author(author_id: int, author_schema: schemas.AuthorPatch, session: AsyncSession = ses_dep):
    return await crud.patch_author_session(session, author_id, author_schema)


@router.patch("/movies/{movie_id}", response_model=schemas.MovieSchema, dependencies=[admin_or_mod_dep],
              tags=["movie", "update"])
async def update_movie(movie_id: int, movie_schema: schemas.MoviePatch, session: AsyncSession = ses_dep):
    return await crud.patch_movie_session(session, movie_id, movie_schema)


@router.patch("/series/{series_id}", response_model=schemas.SeriesSchema, dependencies=[admin_or_mod_dep],
              tags=["series", "update"])
async def update_series(series_id: int, series_schema: schemas.SeriesPatch, session: AsyncSession = ses_dep):
    return await crud.patch_series_session(session, series_id, series_schema)


@router.patch("/role_setter/{user_id}", tags=["user", "update"], dependencies=[admin_dep])
async def change_user_role(user_id: int, role_to_change: str = Form(...),
                           session: AsyncSession = ses_dep):
    return await crud.change_role_session(session, user_id, role_to_change)
