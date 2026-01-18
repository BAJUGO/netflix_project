from typing import Annotated

from fastapi import Form, APIRouter, Body
from sqlalchemy.ext.asyncio import AsyncSession

from backend.authorization import admin_or_mod_dep, admin_dep
from backend.core import ses_dep

import backend.views_part.global_crud as global_crud
import backend.views_part.schemas as schemas

json_body = Annotated[str, Body()]

router = APIRouter()

# =========================
# AUTHORS
# =========================

@router.delete("/authors/{author_id}", dependencies=[admin_or_mod_dep], tags=["author", "delete"])
async def delete_author(author_id: int, session: AsyncSession = ses_dep):
    return await global_crud.delete_author_session(session=session, author_id=author_id)


# @router.put("/authors/{author_id}", response_model=schemas.AuthorSchema, dependencies=[admin_or_mod_dep],
#             tags=["author", "update"], deprecated=True)
# async def full_update_author(author_id: int, author_schema: schemas.AuthorCreate,
#                              session: AsyncSession = ses_dep):
#     return await global_crud.full_update_author_session(session=session, author_id=author_id, author_schema=author_schema)


@router.patch("/authors/{author_id}", response_model=schemas.AuthorSchema, dependencies=[admin_or_mod_dep],
              tags=["author", "update"])
async def patch_update_author(author_id: int, update_body: json_body, session: AsyncSession = ses_dep):
    return await global_crud.patch_author_session(session=session, author_id=author_id, update_author_body=update_body)


# =========================
# MOVIES
# =========================

@router.delete("/movies/{movie_id}", response_model=str, dependencies=[admin_or_mod_dep],
               tags=["movie", "delete"])
async def delete_movie(movie_id: int, session: AsyncSession = ses_dep):
    return await global_crud.delete_movie_session(session=session, movie_id=movie_id)


# @router.put("/movies/{movie_id}", response_model=schemas.MovieSchema, dependencies=[admin_or_mod_dep],
#             tags=["movie", "update"], deprecated=True)
# async def full_update_movie(movie_id: int, update_body: json_body,
#                             session: AsyncSession = ses_dep):
#     return await global_crud.full_update_movie_session(session=session, movie_id=movie_id, update_movie_body=update_body)


@router.patch("/movies/{movie_id}", response_model=schemas.MovieSchema, dependencies=[admin_or_mod_dep],
              tags=["movie", "update"])
async def patch_update_movie(movie_id: int, update_body: json_body, session: AsyncSession = ses_dep):
    return await global_crud.patch_movie_session(session=session, movie_id=movie_id, update_movie_body=update_body)


# =========================
# SERIES
# =========================

@router.delete("/series/{series_id}", dependencies=[admin_or_mod_dep], tags=["series", "delete"])
async def delete_series(series_id: int, session: AsyncSession = ses_dep):
    return await global_crud.delete_series_session(session=session, series_id=series_id)


# @router.put("/series/{series_id}", response_model=schemas.SeriesSchema, dependencies=[admin_or_mod_dep],
#             tags=["series", "update"], deprecated=True)
# async def full_update_series(series_id: int, series_schema: schemas.SeriesCreate,
#                              session: AsyncSession = ses_dep):
#     return await global_crud.full_update_series_session(session=session, series_id=series_id, series_schema=series_schema)


@router.patch("/series/{series_id}", response_model=schemas.SeriesSchema, dependencies=[admin_or_mod_dep],
              tags=["series", "update"])
async def patch_update_series(series_id: int, update_body: json_body, session: AsyncSession = ses_dep):
    return await global_crud.patch_series_session(session=session, series_id=series_id, update_series_body=update_body)


# =========================
# USERS
# =========================

@router.delete("/delete_account/{user_id}", tags=["user", "delete"], dependencies=[admin_dep])
async def delete_user(user_id: int, session: AsyncSession = ses_dep):
    return await global_crud.delete_user_session(user_id=user_id, session=session)


@router.patch("/role_setter/{user_id}", tags=["user", "update"], dependencies=[admin_dep])
async def change_user_role(user_id: int, role_to_change: json_body,
                           session: AsyncSession = ses_dep):
    print(role_to_change)
    return await global_crud.change_role_session(session=session, user_id=user_id, new_role=role_to_change)
