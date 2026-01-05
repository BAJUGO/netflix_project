from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import project_dir.views_part.crud as crud
import project_dir.views_part.schemas as schemas
from project_dir.authorization import admin_or_mod_dep, encode_access_token, get_current_user_access_token, admin_dep, \
    AccessTokenData
from project_dir.authorization.token_enc_dec import encode_refresh_token
from project_dir.authorization.utilites import authenticate_user
from project_dir.core import ses_dep
from project_dir.loging_and_exc.pre_post_up import get_redis

router = APIRouter(dependencies=[])


@router.post("/authors/add_author", response_model=schemas.AuthorSchema, dependencies=[admin_or_mod_dep],
             tags=["author", "add"])
async def add_author(author_in: schemas.AuthorCreate, session: AsyncSession = ses_dep):
    return await crud.add_author_session(author_in, session)


@router.post("/movies/add_movie", response_model=schemas.MovieSchema, dependencies=[admin_or_mod_dep],
             tags=["movie", "add"])
async def add_movie(movie_in: schemas.MovieCreate, session: AsyncSession = ses_dep):
    return await crud.add_movie_session(movie_in, session)


@router.post("/series/add_series", response_model=schemas.SeriesSchema, dependencies=[admin_or_mod_dep],
             tags=["series", "add"])
async def add_series(series_in: schemas.SeriesCreate, session: AsyncSession = ses_dep):
    return await crud.add_series_session(series_in, session)


@router.post("/create_token", tags=["token"])
async def check_function(user=Depends(authenticate_user)):
    data_for_token = {"sub": str(user.id), "name": user.visible_name, "role": user.role, "id": user.id}
    access_token = encode_access_token(data=data_for_token)
    refresh_token = encode_refresh_token(data=data_for_token)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/register", tags=["user", "add"])
async def add_new_user(user_in: schemas.UserCreate, session: AsyncSession = ses_dep):
    return await crud.add_user_session(user_in, session)


@router.get("/authors/get_authors", response_model=list[schemas.AuthorSchema], tags=["author", "get"],
            dependencies=[Depends(get_current_user_access_token)])
async def get_authors(session: AsyncSession = ses_dep):
    return await crud.get_authors_session(session)


@router.get("/movies/get_movies", response_model=list[schemas.MovieSchema], tags=["movie", "get"],
            dependencies=[Depends(get_current_user_access_token)])
async def get_movies(session: AsyncSession = ses_dep):
    return await crud.get_movies_session(session)


@router.get("/series/get_series", response_model=list[schemas.SeriesSchema], tags=["series", "get"],
            dependencies=[Depends(get_current_user_access_token)])
async def get_series(session: AsyncSession = ses_dep):
    return await crud.get_series_session(session)


@router.get("/users/get_users", response_model=list[str], tags=["user", "get"], dependencies=[admin_dep])
async def get_users(session: AsyncSession = ses_dep):
    return await crud.get_users_session(session)


@router.get("/authors/series", tags=["author", "get"], dependencies=[Depends(get_current_user_access_token)])
async def author_series(session: AsyncSession = ses_dep):
    return await crud.get_author_series_session(session)


@router.get("/authors/{author_id}", tags=["author", "get"])
async def get_author(author_id: int, session: AsyncSession = ses_dep, redis=Depends(get_redis)):
    return await crud.get_author_with_cache(author_id=author_id, redis=redis, session=session)


@router.get("/for_users_only", tags=["token"])
async def return_user_token_info(user_token: AccessTokenData = Depends(get_current_user_access_token)):
    return f"Hello {user_token.name}! Your role is {user_token.role} Your id is {user_token.id}"


@router.get("/for_admins_only", tags=["token"])
async def return_admin_token_info(user_token: AccessTokenData = admin_dep):
    return f"Hello admin! Your name is {user_token.name}"
