from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

import project_dir.authorization as auth
import project_dir.views_part.global_crud as global_crud
import project_dir.views_part.global_crud.cached_crud as cached_crud
import project_dir.views_part.schemas as schemas
from project_dir.core import ses_dep
from project_dir.logging_and_exc.pre_post_up import get_redis
from project_dir.routers.delete_put_patch_router import json_body

router = APIRouter(dependencies=[])


# ====================
# TOKEN
# ====================

@router.post("/create_token", tags=["token"])
async def create_token(response: Response, user=Depends(auth.authenticate_user)):
    data = {"sub": str(user.id), "name": user.visible_name, "role": user.role, "id": user.id}
    access_token = auth.encode_access_token(data=data)
    refresh_token = auth.encode_refresh_token(data=data)
    response.set_cookie(key="access_token", value=access_token, max_age=60 * 15, httponly=True, samesite="lax", path="/")
    response.set_cookie(key="refresh_token", value=refresh_token, max_age=60 * 60 * 24 * 7, httponly=True, samesite="lax", path="/")
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/for_users_only", tags=["token"])
async def get_current_user_token_info(user_token: auth.AccessTokenData = Depends(auth.get_current_user_access_token)):
    return f"Hello {user_token.name}! Your role is {user_token.role} Your id is {user_token.id}"


@router.get("/for_admins_only", tags=["token"])
async def get_admin_token_info(user_token: auth.AccessTokenData = auth.admin_dep):
    return f"Hello admin! Your name is {user_token.name}"


# ====================
# USERS
# ====================

@router.post("/register", tags=["user", "add"])
async def create_user(user_in_body: json_body, session: AsyncSession = ses_dep):
    return await global_crud.add_user_session(user_in_body=user_in_body, session=session)


@router.get("/users/get_users", response_model=list, tags=["user", "get"], dependencies=[auth.admin_dep])
async def get_all_users(session: AsyncSession = ses_dep):
    return await global_crud.get_users_session(session)


@router.get("/users/{user_id}", response_model=schemas.UserSchema, tags=["user", "get"])
async def get_user_by_id(user_id: int, session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await cached_crud.get_user_by_id_with_cache(session=session, redis=redis, user_id=user_id)


# ====================
# AUTHORS
# ====================

@router.post("/authors/add_author", response_model=schemas.AuthorSchema, dependencies=[auth.admin_or_mod_dep], tags=["author", "add"])
async def create_author(new_body: json_body, session: AsyncSession = ses_dep):
    return await global_crud.add_author_session(session=session, new_author_body=new_body)


@router.get("/authors/get_authors", response_model=list[schemas.AuthorSchema], tags=["author", "get"], dependencies=[Depends(auth.get_current_user_access_token)])
async def get_all_authors(session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await cached_crud.get_all_authors_with_cache(session=session, redis=redis, second_key_arg="all")


@router.get("/authors/series", response_model=dict[str, list], tags=["author", "get"], dependencies=[Depends(auth.get_current_user_access_token)])
async def get_authors_series(session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await cached_crud.get_authors_and_their_series_with_cache(session=session, redis=redis, second_key_arg="series")


@router.get("/authors/movies", response_model=dict[str, list], tags=["author", "get"], dependencies=[Depends(auth.get_current_user_access_token)])
async def get_authors_movies(session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await cached_crud.get_authors_and_their_movies_with_cache(session=session, redis=redis, second_key_arg="movies")


@router.get("/authors/{author_id}", tags=["author", "get"])
async def get_author_by_id(author_id: int, session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await cached_crud.get_author_by_id_with_cache(session=session, redis=redis, author_id=author_id)


# ====================
# MOVIES
# ====================

@router.post("/movies/add_movie", response_model=schemas.MovieSchema, dependencies=[auth.admin_or_mod_dep], tags=["movie", "add"])
async def create_movie(new_body: json_body, session: AsyncSession = ses_dep):
    return await global_crud.add_movie_session(session=session, new_movie_body=new_body)


@router.get("/movies/get_movies", response_model=list[schemas.MovieSchema], tags=["movie", "get"], dependencies=[Depends(auth.get_current_user_access_token)])
async def get_all_movies(session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await cached_crud.get_all_movies_with_cache(session=session, redis=redis, second_key_arg="all")


@router.get("/movies/{movie_id}", tags=["movie", "get"])
async def get_movie_by_id(movie_id: int, session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await cached_crud.get_movie_by_id_with_cache(session=session, redis=redis, movie_id=movie_id)


@router.get("/movies/{movie_id}/author", tags=["movie", "get"])
async def get_movie_author(movie_id: int, session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await cached_crud.get_author_of_movie_with_cache(session=session, redis=redis, movie_id=movie_id, second_key_arg="author")


# ====================
# SERIES
# ====================

@router.post("/series/add_series", response_model=schemas.SeriesSchema, dependencies=[auth.admin_or_mod_dep], tags=["series", "add"])
async def create_series(new_body: json_body, session: AsyncSession = ses_dep):
    return await global_crud.add_series_session(session=session, new_series_body=new_body)


@router.get("/series/get_series", response_model=list[schemas.SeriesSchema], tags=["series", "get"], dependencies=[Depends(auth.get_current_user_access_token)])
async def get_all_series(session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await cached_crud.get_all_series_with_cache(session=session, redis=redis, second_key_arg="all")


@router.get("/series/{series_id}", tags=["series", "get"])
async def get_series_by_id(series_id: int, session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await cached_crud.get_series_by_id_with_cache(session=session, redis=redis, series_id=series_id)


@router.get("/series/{series_id}/author", tags=["series", "get"])
async def get_series_author(series_id: int, session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await cached_crud.get_author_of_series_with_cache(session=session, redis=redis, series_id=series_id, second_key_arg="author")
