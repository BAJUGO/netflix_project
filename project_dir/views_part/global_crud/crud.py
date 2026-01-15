import json
from typing import TypeVar, Annotated

from fastapi import HTTPException, Body
from pydantic import BaseModel
from sqlalchemy import Select, update
from sqlalchemy.ext.asyncio import AsyncSession

from project_dir.authorization import hash_password
from project_dir.models import Author, Movie, Series, User
import project_dir.views_part.schemas as schemas

T = TypeVar("T", Movie, Series, Author, User)
P = TypeVar("P", bound=BaseModel)


# =========================
# HELPERS (ORM -> SCHEMA)
# =========================

async def models_to_schemas(list_of_models: list[T], schema: type[P]) -> list[P]:
    return [schema.model_validate(model).model_dump() for model in list_of_models]


async def model_to_schema(model: T, schema: type[P]) -> P:
    return schema.model_validate(model).model_dump()


# =========================
# BASE DB OPERATIONS (ORM)
# =========================

async def adder_session(session: AsyncSession, data: dict, orm_model: type[T]) -> T:
    obj = orm_model(**data)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def getter_session(session: AsyncSession, orm_model: type[T]) -> list[T]:
    stmt = Select(orm_model).order_by(orm_model.id)
    objs = list(await session.scalars(stmt))
    if objs:
        return objs
    raise HTTPException(status_code=404, detail=f"There are no {orm_model.__name__} at all!")


async def getter_by_id_session(session: AsyncSession, orm_model: type[T], obj_id: int) -> T:
    obj = await session.get(orm_model, obj_id)
    if obj:
        return obj
    raise HTTPException(status_code=404, detail=f"{orm_model.__name__} wasn't found")


async def deleter_session(session: AsyncSession, orm_model: type[T], obj_id: int) -> None:
    obj = await getter_by_id_session(session=session, orm_model=orm_model, obj_id=obj_id)
    await session.delete(obj)
    await session.commit()


async def patch_updater_session(session: AsyncSession, orm_model: type[T], obj_id: int, schema_patch: P) -> T:
    await session.execute(update(orm_model).where(orm_model.id == obj_id).values(**schema_patch.model_dump(exclude_unset=True)))
    await session.commit()
    return await getter_by_id_session(session=session, orm_model=orm_model, obj_id=obj_id)


async def full_updater_session(session: AsyncSession, orm_model: type[T], obj_id: int, schema_patch: P) -> T:
    await session.execute(update(orm_model).where(orm_model.id == obj_id).values(**schema_patch.model_dump(exclude_unset=False)))
    await session.commit()
    return await getter_by_id_session(session=session, orm_model=orm_model, obj_id=obj_id)


# =========================
# GET BY ID
# =========================

async def get_author_by_id_session(session: AsyncSession, author_id: int):
    author = await getter_by_id_session(session=session, orm_model=Author, obj_id=author_id)
    return await model_to_schema(author, schemas.AuthorSchema)


async def get_movie_by_id_session(session: AsyncSession, movie_id: int):
    movie = await getter_by_id_session(session=session, orm_model=Movie, obj_id=movie_id)
    return await model_to_schema(movie, schemas.MovieSchema)


async def get_series_by_id_session(session: AsyncSession, series_id: int):
    series = await getter_by_id_session(session=session, orm_model=Series, obj_id=series_id)
    return await model_to_schema(series, schemas.SeriesSchema)


async def get_user_by_id_session(session: AsyncSession, user_id: int):
    user = await getter_by_id_session(session=session, orm_model=User, obj_id=user_id)
    return await model_to_schema(user, schemas.UserSchema)

# =========================
# ADD
# =========================

async def add_author_session(session: AsyncSession, author_in: schemas.AuthorCreate) -> schemas.AuthorSchema:
    author = await adder_session(session=session, data=author_in, orm_model=Author)
    return await model_to_schema(author, schemas.AuthorSchema)


async def add_movie_session(session: AsyncSession, movie_body: Annotated[str, Body()]) -> schemas.MovieSchema:
    movie_body_json = json.loads(movie_body)
    movie_in = movie_body_json["movie_body"]
    movie = await adder_session(session=session, data=movie_in, orm_model=Movie)
    return await model_to_schema(movie, schemas.MovieSchema)


async def add_series_session(session: AsyncSession, series_in: schemas.SeriesCreate) -> schemas.SeriesSchema:
    series = await adder_session(session=session, data=series_in, orm_model=Series)
    return await model_to_schema(series, schemas.SeriesSchema)


async def add_user_session(session: AsyncSession, user_in: schemas.UserCreate) -> schemas.UserSchema:
    user = User(**user_in.model_dump(exclude={"password"}), hashed_password=hash_password(user_in.password), role="user", active=True)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return await model_to_schema(user, schemas.UserSchema)


# =========================
# DELETE
# =========================

async def delete_user_session(session: AsyncSession, user_id: int) -> str:
    await deleter_session(session=session, orm_model=User, obj_id=user_id)
    return f"User with id {user_id} has been deleted"


async def delete_author_session(session: AsyncSession, author_id: int) -> str:
    await deleter_session(session=session, orm_model=Author, obj_id=author_id)
    return f"Author with id {author_id} has been deleted"


async def delete_series_session(session: AsyncSession, series_id: int) -> str:
    await deleter_session(session=session, orm_model=Series, obj_id=series_id)
    return f"Series with id {series_id} has been deleted"


async def delete_movie_session(session: AsyncSession, movie_id: int) -> str:
    await deleter_session(session=session, orm_model=Movie, obj_id=movie_id)
    return f"Movie with id {movie_id} has been deleted"


# =========================
# GET LISTS
# =========================

async def get_authors_session(session: AsyncSession) -> list[schemas.AuthorSchema]:
    return await models_to_schemas(await getter_session(session=session, orm_model=Author), schemas.AuthorSchema)


async def get_movies_session(session: AsyncSession) -> list[schemas.MovieSchema]:
    return await models_to_schemas(await getter_session(session=session, orm_model=Movie), schemas.MovieSchema)


async def get_series_session(session: AsyncSession) -> list[schemas.SeriesSchema]:
    return await models_to_schemas(await getter_session(session=session, orm_model=Series), schemas.SeriesSchema)


async def get_users_session(session: AsyncSession) -> list[str]:
    return [user.visible_name for user in await getter_session(session=session, orm_model=User)]


# =========================
# CHANGE ROLE
# =========================

async def change_role_session(session: AsyncSession, user_id: int, new_role: str) -> str:
    user = await getter_by_id_session(session=session, orm_model=User, obj_id=user_id)
    user.role = new_role
    await session.commit()
    await session.refresh(user)
    return f"{user.visible_name} role has been changed to {user.role}"


# =========================
# PATCH
# =========================

async def patch_author_session(session: AsyncSession, author_id: int, author_schema: schemas.AuthorPatch) -> schemas.AuthorSchema:
    return await model_to_schema(await patch_updater_session(session=session, orm_model=Author, obj_id=author_id, schema_patch=author_schema), schemas.AuthorSchema)


async def patch_movie_session(session: AsyncSession, movie_id: int, movie_schema: schemas.MoviePatch) -> schemas.MovieSchema:
    return await model_to_schema(await patch_updater_session(session=session, orm_model=Movie, obj_id=movie_id, schema_patch=movie_schema), schemas.MovieSchema)


async def patch_series_session(session: AsyncSession, series_id: int, series_schema: schemas.SeriesPatch) -> schemas.SeriesSchema:
    return await model_to_schema(await patch_updater_session(session=session, orm_model=Series, obj_id=series_id, schema_patch=series_schema), schemas.SeriesSchema)


# =========================
# FULL UPDATE
# =========================

async def full_update_author_session(session: AsyncSession, author_id: int, author_schema: schemas.AuthorCreate) -> schemas.AuthorSchema:
    return await model_to_schema(await full_updater_session(session=session, orm_model=Author, obj_id=author_id, schema_patch=author_schema), schemas.AuthorSchema)


async def full_update_movie_session(session: AsyncSession, movie_id: int, movie_schema: schemas.MovieCreate) -> schemas.MovieSchema:
    return await model_to_schema(await full_updater_session(session=session, orm_model=Movie, obj_id=movie_id, schema_patch=movie_schema), schemas.MovieSchema)


async def full_update_series_session(session: AsyncSession, series_id: int, series_schema: schemas.SeriesCreate) -> schemas.SeriesSchema:
    return await model_to_schema(await full_updater_session(session=session, orm_model=Series, obj_id=series_id, schema_patch=series_schema), schemas.SeriesSchema)
