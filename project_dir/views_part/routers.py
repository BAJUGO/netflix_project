import redis.asyncio
from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

from project_dir.authorization import get_current_user_access_token, admin_or_mod_dep, encode_access_token, \
    AccessTokenData, admin_dep
from project_dir.authorization.token_enc_dec import encode_refresh_token
from project_dir.authorization.utilites import authenticate_user
from project_dir.core import ses_dep
from project_dir.models import Author
from project_dir.views_part.cached_crud import cache_object_with_id
from project_dir.views_part.crud import (
    add_author_session,
    add_movie_session,
    get_authors_session,
    get_movies_session,
    delete_author_session,
    add_series_session,
    get_series_session,
    delete_movie_session,
    delete_series_session,
    get_users_session,
    full_update_author_session,
    full_update_movie_session,
    full_update_series_session,
    patch_movie_session,
    patch_author_session,
    patch_series_session,
    add_user_session,
    delete_user_session,
    change_role_session
)
from project_dir.views_part.relationship_crud import get_author_series_session
from project_dir.views_part.schemas import (
    AuthorCreate,
    AuthorSchema,
    MovieSchema,
    MovieCreate,
    SeriesCreate,
    SeriesSchema, MoviePatch, SeriesPatch, AuthorPatch, UserCreate
)

rd = redis.asyncio.Redis(host="localhost", port=6379, db=0)

router = APIRouter(dependencies=[])


@router.post("/authors/add_author", response_model=AuthorSchema, dependencies=[admin_or_mod_dep],
             tags=["author", "add"])
async def add_author(author_in: AuthorCreate, session: AsyncSession = ses_dep):
    return await add_author_session(author_in, session)


@router.post("/movies/add_movie", response_model=MovieSchema, dependencies=[admin_or_mod_dep], tags=["movie", "add"])
async def add_movie(movie_in: MovieCreate, session: AsyncSession = ses_dep):
    return await add_movie_session(movie_in, session)


@router.post("/series/add_series", response_model=SeriesSchema, dependencies=[admin_or_mod_dep], tags=["series", "add"])
async def add_series(series_in: SeriesCreate, session: AsyncSession = ses_dep):
    return await add_series_session(series_in, session)


@router.post("/create_token", tags=["token"])
async def check_function(user=Depends(authenticate_user)):
    data_for_token = {"sub": str(user.id), "name": user.visible_name, "role": user.role, "id": user.id}
    access_token = encode_access_token(data=data_for_token)
    refresh_token = encode_refresh_token(data=data_for_token)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/register", tags=["user", "add"])
async def add_new_user(user_in: UserCreate, session: AsyncSession = ses_dep):
    return await add_user_session(user_in, session)


@router.get("/authors/get_authors", response_model=list[AuthorSchema], tags=["author", "get"],
            dependencies=[Depends(get_current_user_access_token)])
async def get_authors(session: AsyncSession = ses_dep):
    return await get_authors_session(session)


@router.get("/movies/get_movies", response_model=list[MovieSchema], tags=["movie", "get"],
            dependencies=[Depends(get_current_user_access_token)])
async def get_movies(session: AsyncSession = ses_dep):
    return await get_movies_session(session)


@router.get("/series/get_series", response_model=list[SeriesSchema], tags=["series", "get"],
            dependencies=[Depends(get_current_user_access_token)])
async def get_series(session: AsyncSession = ses_dep):
    return await get_series_session(session)


@router.get("/users/get_users", response_model=list[str], tags=["user", "get"], dependencies=[admin_dep])
async def get_users(session: AsyncSession = ses_dep):
    return await get_users_session(session)


@router.get("/authors/{author_id}")
async def get_author(author_id: int, session: AsyncSession = ses_dep):
    return await cache_object_with_id(rd=rd, session=session, obj_id=author_id, orm_model=Author, ex=30)


@router.get("/for_users_only", tags=["token"])
async def return_user_token_info(user_token: AccessTokenData = Depends(get_current_user_access_token)):
    return f"Hello {user_token.name}! Your role is {user_token.role} Your id is {user_token.id}"


@router.get("/authors/series", tags=["author", "get"], dependencies=[Depends(get_current_user_access_token)])
async def author_series(session: AsyncSession = ses_dep):
    return await get_author_series_session(session)


@router.get("/for_admins_only", tags=["token"])
async def return_admin_token_info(user_token: AccessTokenData = admin_dep):
    return f"Hello admin! Your name is {user_token.name}"


@router.delete("/authors/{author_id}", dependencies=[admin_or_mod_dep], tags=["author", "delete"])
async def delete_author(author_id: int, session: AsyncSession = ses_dep):
    return await delete_author_session(session, author_id)


@router.delete("/series/{series_id}", dependencies=[admin_or_mod_dep], tags=["movie", "delete"])
async def delete_series(series_id: int, session: AsyncSession = ses_dep):
    return await delete_series_session(session, series_id)


@router.delete("/movies/{movie_id}", response_model=MovieSchema, dependencies=[admin_or_mod_dep],
               tags=["series", "delete"])
async def delete_movie(movie_id: int, session: AsyncSession = ses_dep):
    return await delete_movie_session(session, movie_id)


@router.delete("/delete_account", tags=["user", "delete"], dependencies=[admin_dep])
async def delete_user(user_id: int, session: AsyncSession = ses_dep):
    return await delete_user_session(user_to_delete_id=user_id, session=session)


@router.put("/authors/{author_id}", response_model=AuthorSchema, dependencies=[admin_or_mod_dep],
            tags=["author", "update"])
async def update_author(author_id: int, author_schema: AuthorCreate, session: AsyncSession = ses_dep):
    return await full_update_author_session(session, author_id, author_schema)


@router.put("/movies/{movie_id}", response_model=MovieSchema, dependencies=[admin_or_mod_dep],
            tags=["movie", "update"])
async def full_update_movie(movie_id: int, movie_schema: MovieCreate, session: AsyncSession = ses_dep):
    return await full_update_movie_session(session, movie_id, movie_schema)


@router.put("/series/{series_id}", response_model=SeriesSchema, dependencies=[admin_or_mod_dep],
            tags=["series", "update"])
async def full_update_series(series_id: int, series_schema: SeriesCreate, session: AsyncSession = ses_dep):
    return await full_update_series_session(session, series_id, series_schema)


@router.patch("/authors/{author_id}", response_model=AuthorSchema, dependencies=[admin_or_mod_dep],
              tags=["author", "update"])
async def update_author(author_id: int, author_schema: AuthorPatch, session: AsyncSession = ses_dep):
    return await patch_author_session(session, author_id, author_schema)


@router.patch("/movies/{movie_id}", response_model=MovieSchema, dependencies=[admin_or_mod_dep],
              tags=["movie", "update"])
async def update_movie(movie_id: int, movie_schema: MoviePatch, session: AsyncSession = ses_dep):
    return await patch_movie_session(session, movie_id, movie_schema)


@router.patch("/series/{series_id}", response_model=SeriesSchema, dependencies=[admin_or_mod_dep],
              tags=["series", "update"])
async def update_series(series_id: int, series_schema: SeriesPatch, session: AsyncSession = ses_dep):
    return await patch_series_session(session, series_id, series_schema)


@router.patch("/role_setter/{user_id}", tags=["user", "update"], dependencies=[admin_dep])
async def change_user_role(user_id: int, role_to_change: str = Form(...),
                           session: AsyncSession = ses_dep):
    return await change_role_session(session, user_id, role_to_change)
