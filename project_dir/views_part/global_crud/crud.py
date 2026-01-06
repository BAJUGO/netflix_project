from typing import TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Select, update
from sqlalchemy.ext.asyncio import AsyncSession

from project_dir.authorization import hash_password
from project_dir.models import Author, Movie, Series, User
from project_dir.views_part.schemas import (
    AuthorCreate,
    MovieCreate,
    UserCreate,
    SeriesCreate,
    MoviePatch,
    SeriesPatch,
    AuthorPatch,
)

T = TypeVar("T", Movie, Series, Author, User)
P = TypeVar("P", bound=BaseModel)


async def adder_session(
    data: BaseModel, session: AsyncSession, orm_model: type[T]
) -> T:
    obj = orm_model(**data.model_dump())
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def getter_session(session: AsyncSession, orm_model: type[T]) -> list[T]:
    stmt = Select(orm_model).order_by(orm_model.id)
    result = await session.scalars(stmt)
    if result:
        return list(result)
    raise HTTPException(status_code=404, detail=f"There are no {orm_model.__name__} at all!")

async def getter_by_id_session(
    session: AsyncSession, orm_model: type[T], obj_id: int
) -> T:
    obj = await session.get(orm_model, obj_id)
    if obj:
        return obj
    raise HTTPException(status_code=404, detail=f"{orm_model.__name__} wasn't found")



async def deleter_session(
    session: AsyncSession, obj_id: int, orm_model: type[T]
) -> None:
    obj_to_del = await getter_by_id_session(
        session=session, orm_model=orm_model, obj_id=obj_id
    )
    await session.delete(obj_to_del)
    await session.commit()


async def patch_updater_session(
    session: AsyncSession, obj_id: int, orm_model: type[T], schema_patch: P
) -> T:
    data_to_update = schema_patch.model_dump(exclude_unset=True)
    await session.execute(
        update(orm_model).where(orm_model.id == obj_id).values(**data_to_update)
    )
    await session.commit()
    return await getter_by_id_session(session, orm_model, obj_id)


async def full_updater_session(
    session: AsyncSession, obj_id: int, orm_model: type[T], schema_patch: P
) -> T:
    data_to_update = schema_patch.model_dump(exclude_unset=False)
    await session.execute(
        update(orm_model).where(orm_model.id == obj_id).values(**data_to_update)
    )
    await session.commit()
    return await getter_by_id_session(session, orm_model, obj_id)


# ! ADD
async def add_author_session(author_in: AuthorCreate, session: AsyncSession) -> Author:
    return await adder_session(data=author_in, session=session, orm_model=Author)


async def add_movie_session(movie_in: MovieCreate, session: AsyncSession) -> Movie:
    return await adder_session(movie_in, session, Movie)


async def add_series_session(series_in: SeriesCreate, session: AsyncSession) -> Series:
    return await adder_session(series_in, session, Series)


async def add_user_session(user_in: UserCreate, session: AsyncSession) -> str:
    user = User(
        **user_in.model_dump(exclude={"password"}),
        hashed_password=hash_password(user_in.password),
        role="user",
        active=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return (
        f"Hello user {user.visible_name}! You have registered, and your ID is {user.id}"
    )


# ! DEL
async def delete_user_session(session: AsyncSession, user_to_delete_id: int) -> str:
    await deleter_session(session=session, obj_id=user_to_delete_id, orm_model=User)
    return f"User with id {user_to_delete_id} has been deleted"


async def delete_author_session(session: AsyncSession, author_to_delete_id: int) -> str:
    await deleter_session(session, author_to_delete_id, Author)
    return f"Author with id {author_to_delete_id} has been deleted"


async def delete_series_session(session: AsyncSession, series_to_delete_id: int) -> str:
    await deleter_session(session, series_to_delete_id, Series)
    return f"Series with id {series_to_delete_id} has been deleted"


async def delete_movie_session(session: AsyncSession, movie_to_delete_id: int) -> str:
    await deleter_session(session, movie_to_delete_id, Movie)
    return f"Movie with id {movie_to_delete_id} has been deleted"


# ! GET_LISTS
async def get_authors_session(session: AsyncSession) -> list[Author]:
    return await getter_session(session, Author)


async def get_movies_session(session: AsyncSession) -> list[Movie]:
    return await getter_session(session, Movie)


async def get_series_session(session: AsyncSession) -> list[Series]:
    return await getter_session(session, Series)


async def get_users_session(session: AsyncSession) -> list[str]:
    return [user.visible_name for user in (await getter_session(session, User))]


# ! CHANGE_ROLE
async def change_role_session(
    session: AsyncSession, user_id: int, new_role: str
) -> str:
    user = await getter_by_id_session(session, User, user_id)
    user.role = new_role
    await session.commit()
    await session.refresh(user)
    return f"{user.visible_name} role has been changed to {user.role}"


# ! PATCH
async def patch_author_session(
    session: AsyncSession, author_id: int, author_schema: AuthorPatch
) -> Author:
    return await patch_updater_session(session, author_id, Author, author_schema)


async def patch_movie_session(
    session: AsyncSession, movie_id: int, movie_schema: MoviePatch
) -> Movie:
    return await patch_updater_session(session, movie_id, Movie, movie_schema)


async def patch_series_session(
    session: AsyncSession, series_id: int, series_schema: SeriesPatch
) -> Series:
    return await patch_updater_session(session, series_id, Series, series_schema)


# ! FULL_UPDATE
async def full_update_author_session(
    session: AsyncSession, author_id: int, author_schema: AuthorCreate
) -> Author:
    return await full_updater_session(session, author_id, Author, author_schema)


async def full_update_movie_session(
    session: AsyncSession, movie_id: int, movie_schema: MovieCreate
) -> Movie:
    return await full_updater_session(session, movie_id, Movie, movie_schema)


async def full_update_series_session(
    session: AsyncSession, series_id: int, series_schema: SeriesCreate
) -> Series:
    return await full_updater_session(session, series_id, Series, series_schema)
