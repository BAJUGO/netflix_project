from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import project_dir.views_part.global_crud as global_crud
import project_dir.views_part.schemas as schemas

import project_dir.authorization as auth
from project_dir.core import ses_dep
from project_dir.logging_and_exc.pre_post_up import get_redis

router = APIRouter(dependencies=[])

# =========================
# AUTH / TOKEN
# =========================

@router.post("/create_token", tags=["token"])
async def create_token(user=Depends(auth.authenticate_user)):
    data_for_token = {"sub": str(user.id), "name": user.visible_name, "role": user.role, "id": user.id}
    access_token = auth.encode_access_token(data=data_for_token)
    refresh_token = auth.encode_refresh_token(data=data_for_token)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/for_users_only", tags=["token"])
async def get_current_user_token_info(
    user_token: auth.AccessTokenData = Depends(auth.get_current_user_access_token),
):
    return f"Hello {user_token.name}! Your role is {user_token.role} Your id is {user_token.id}"


@router.get("/for_admins_only", tags=["token"])
async def get_admin_token_info(user_token: auth.AccessTokenData = auth.admin_dep):
    return f"Hello admin! Your name is {user_token.name}"


# =========================
# USERS
# =========================

@router.post("/register", tags=["user", "add"])
async def create_user(user_in: schemas.UserCreate, session: AsyncSession = ses_dep):
    return await global_crud.add_user_session(user_in, session)


@router.get("/users/get_users", response_model=list[str], tags=["user", "get"], dependencies=[auth.admin_dep])
async def get_all_users(session: AsyncSession = ses_dep):
    return await global_crud.get_users_session(session)


# =========================
# AUTHORS
# =========================

@router.post("/authors/add_author", response_model=schemas.AuthorSchema, dependencies=[auth.admin_or_mod_dep],
             tags=["author", "add"])
async def create_author(author_in: schemas.AuthorCreate, session: AsyncSession = ses_dep):
    return await global_crud.add_author_session(author_in, session)


@router.get("/authors/get_authors", response_model=list[schemas.AuthorSchema], tags=["author", "get"],
            dependencies=[Depends(auth.get_current_user_access_token)])
async def get_all_authors(session: AsyncSession = ses_dep):
    return await global_crud.get_authors_session(session)


@router.get("/authors/series", response_model=dict[str, list], tags=["author", "get"],
            dependencies=[Depends(auth.get_current_user_access_token)])
async def get_all_authors_with_series(session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await global_crud.get_author_series_with_cache(series="series", redis=redis, session=session)


@router.get("/authors/{author_id}", tags=["author", "get"])
async def get_author_by_id(author_id: int, session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await global_crud.get_author_with_cache(author_id=author_id, redis=redis, session=session)


# =========================
# MOVIES
# =========================

@router.post("/movies/add_movie", response_model=schemas.MovieSchema, dependencies=[auth.admin_or_mod_dep],
             tags=["movie", "add"])
async def create_movie(movie_in: schemas.MovieCreate, session: AsyncSession = ses_dep):
    return await global_crud.add_movie_session(movie_in, session)


@router.get("/movies/get_movies", response_model=list[schemas.MovieSchema], tags=["movie", "get"],
            dependencies=[Depends(auth.get_current_user_access_token)])
async def get_all_movies(session: AsyncSession = ses_dep):
    return await global_crud.get_movies_session(session)


@router.get("/movies/{movie_id}", tags=["movie", "get"])
async def get_movie_by_id(movie_id: int, session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await global_crud.get_movie_with_cache(redis=redis, session=session, movie_id=movie_id)


@router.get("/movies/{movie_id}/author", tags=["movie", "get"])
async def get_movie_author_by_movie_id(
    movie_id: int,
    session: AsyncSession = ses_dep,
    redis=Depends(get_redis),
):
    return await global_crud.get_author_of_movie_with_cache(
        redis=redis,
        session=session,
        movie_id=movie_id,
        second_key_arg="author",
    )


# =========================
# SERIES
# =========================

@router.post("/series/add_series", response_model=schemas.SeriesSchema, dependencies=[auth.admin_or_mod_dep],
             tags=["series", "add"])
async def create_series(series_in: schemas.SeriesCreate, session: AsyncSession = ses_dep):
    return await global_crud.add_series_session(series_in, session)


@router.get("/series/get_series", response_model=list[schemas.SeriesSchema], tags=["series", "get"],
            dependencies=[Depends(auth.get_current_user_access_token)])
async def get_all_series(session: AsyncSession = ses_dep):
    return await global_crud.get_series_session(session)


@router.get("/series/{series_id}", tags=["series", "get"])
async def get_series_by_id(series_id: int, session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await global_crud.get_series_with_cache(redis=redis, session=session, series_id=series_id)


@router.get("/series/{series_id}/author", tags=["series", "get"])
async def get_series_author_by_series_id(
    series_id: int,
    session: AsyncSession = ses_dep,
    redis=Depends(get_redis),
):
    return await global_crud.get_author_of_series_with_cache(
        redis=redis,
        session=session,
        series_id=series_id,
        second_key_arg="author",
    )
