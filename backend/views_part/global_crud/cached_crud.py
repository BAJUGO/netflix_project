import json
from functools import wraps
from typing import Callable

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

import project_dir.views_part.global_crud.crud as default_crud
import project_dir.views_part.global_crud.relationship_crud as rel_crud


def cache_response_wrapper(ttl: int, namespace: str, key_builder: Callable[[dict], str] | None = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis: Redis | None = kwargs.get("redis")
            if not redis or not key_builder:
                return await func(*args, **kwargs)
            cache_key = f"{namespace}:{key_builder(kwargs)}"
            try:
                if cached := await redis.get(cache_key):
                    return json.loads(cached)
            except Exception as e:
                print(f"exception with caching! {e}")
            response = await func(*args, **kwargs)
            try:
                await redis.set(cache_key, json.dumps(response), ex=ttl)
            except Exception as e:
                print(f"exception with caching! {e}")
            return response
        return wrapper
    return decorator


@cache_response_wrapper(30, "author", lambda kw: str(kw["author_id"]))
async def get_author_by_id_with_cache(session: AsyncSession, redis: Redis | None, author_id: int):
    return await default_crud.get_author_by_id_session(session, author_id)


@cache_response_wrapper(30, "movie", lambda kw: str(kw["movie_id"]))
async def get_movie_by_id_with_cache(session: AsyncSession, redis: Redis | None, movie_id: int):
    return await default_crud.get_movie_by_id_session(session, movie_id)


@cache_response_wrapper(30, "series", lambda kw: str(kw["series_id"]))
async def get_series_by_id_with_cache(session: AsyncSession, redis: Redis | None, series_id: int):
    return await default_crud.get_series_by_id_session(session, series_id)


@cache_response_wrapper(30, "user", lambda kw: str(kw["user_id"]))
async def get_user_by_id_with_cache(session: AsyncSession, redis: Redis | None, user_id: int):
    return await default_crud.get_user_by_id_session(session, user_id)


@cache_response_wrapper(30, "authors", lambda kw: kw["second_key_arg"])
async def get_authors_and_their_series_with_cache(session: AsyncSession, redis: Redis | None, second_key_arg: str = "series"):
    return await rel_crud.get_series_of_author_rel_session(session)


@cache_response_wrapper(30, "authors", lambda kw: kw["second_key_arg"])
async def get_authors_and_their_movies_with_cache(session: AsyncSession, redis: Redis | None, second_key_arg: str = "movies"):
    return await rel_crud.get_movies_of_author_rel_session(session)


@cache_response_wrapper(180, "movie", lambda kw: f'{kw["movie_id"]}:{kw["second_key_arg"]}')
async def get_author_of_movie_with_cache(session: AsyncSession, redis: Redis | None, movie_id: int, second_key_arg: str = "author"):
    return await rel_crud.get_author_of_movie_rel_session(session, movie_id)


@cache_response_wrapper(180, "series", lambda kw: f'{kw["series_id"]}:{kw["second_key_arg"]}')
async def get_author_of_series_with_cache(session: AsyncSession, redis: Redis | None, series_id: int, second_key_arg: str = "author"):
    return await rel_crud.get_author_of_series_rel_session(session, series_id)


@cache_response_wrapper(60, "authors", lambda kw: kw["second_key_arg"])
async def get_all_authors_with_cache(session: AsyncSession, redis: Redis | None, second_key_arg: str = "all"):
    return await default_crud.get_authors_session(session)


@cache_response_wrapper(60, "movies", lambda kw: kw["second_key_arg"])
async def get_all_movies_with_cache(session: AsyncSession, redis: Redis | None, second_key_arg: str = "all"):
    return await default_crud.get_movies_session(session)


@cache_response_wrapper(60, "series", lambda kw: kw["second_key_arg"])
async def get_all_series_with_cache(session: AsyncSession, redis: Redis | None, second_key_arg: str = "all"):
    return await default_crud.get_series_session(session)


@cache_response_wrapper(60, "users", lambda kw: kw["second_key_arg"])
async def get_all_users_with_cache(session: AsyncSession, redis: Redis | None, second_key_arg: str = "all"):
    return await default_crud.get_series_session(session)

