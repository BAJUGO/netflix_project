import json
from functools import wraps
from typing import Callable

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

import project_dir.models as models
import project_dir.views_part.global_crud.crud as default_crud
import project_dir.views_part.global_crud.relationship_crud as rel_crud
import project_dir.views_part.schemas as schemas


def cache_response_wrapper(
        ttl: int, namespace: str, key_builder: Callable[[dict], str] | None = None
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not (cache := kwargs.get("redis")) or not key_builder:
                return await func(*args, **kwargs)

            cache_key = f"{namespace}:{key_builder(kwargs)}"

            try:
                if cached_value := await cache.get(cache_key):
                    return json.loads(cached_value)
            except Exception as e:
                print(f"Couldn't cache this shit! {e}")
            response = await func(*args, **kwargs)
            try:
                await cache.set(name=cache_key, value=json.dumps(response), ex=ttl)
            except Exception as e:
                print(f"Couldn't cache this shit! {e}")
            return response

        return wrapper

    return decorator


# def zatychka(kw):
#     return str(kw["author_id"])
#
# def zatychka2(kw):
#     return kw["content"]
#
# def zatychka3(kw):
#     return f'{kw["movie_id"]}:{kw["second_key_arg"]}'


@cache_response_wrapper(ttl=20, namespace="author", key_builder=lambda kwg_arg: str(kwg_arg["author_id"]))
async def get_author_with_cache(
        redis: Redis | None, session: AsyncSession, author_id: int
):
    author = await default_crud.getter_by_id_session(session, models.Author, author_id)
    return schemas.AuthorSchema.model_validate(author).model_dump()


@cache_response_wrapper(ttl=20, namespace="movie", key_builder=lambda kwg_arg: str(kwg_arg["movie_id"]))
async def get_movie_with_cache(
        redis: Redis | None, session: AsyncSession, movie_id: int
):
    movie = await default_crud.getter_by_id_session(session, models.Movie, movie_id)
    return schemas.MovieSchema.model_validate(movie).model_dump()


@cache_response_wrapper(ttl=20, namespace="series", key_builder=lambda kwg_arg: str(kwg_arg["series_id"]))
async def get_series_with_cache(
        redis: Redis | None, session: AsyncSession, series_id: int
):
    series = await default_crud.getter_by_id_session(session, models.Series, series_id)
    return schemas.SeriesSchema.model_validate(series).model_dump()


@cache_response_wrapper(ttl=30, namespace="authors", key_builder=lambda kwg_arg: kwg_arg["series"])
async def get_author_series_with_cache(
        redis: Redis | None, session: AsyncSession, series: str = "series"
):
    return await rel_crud.get_author_content_session(session, base_class_attribute=models.Author.series,
                                                     schema=schemas.SeriesSchema)


@cache_response_wrapper(ttl=180, namespace="movie",
                        key_builder=lambda kwg_arg: f'{kwg_arg["movie_id"]}:{kwg_arg["second_key_arg"]}')
async def get_author_of_movie_with_cache(
        redis: Redis | None,
        session: AsyncSession,
        movie_id: int,
        second_key_arg: str = "author",
):
    return await rel_crud.get_author_of_content(session=session, base_class=models.Movie,
                                                base_class_author=models.Movie.author,
                                                content_id=movie_id)


@cache_response_wrapper(ttl=180, namespace="series",
                        key_builder=lambda kwg_arg: f'{kwg_arg["series_id"]}:{kwg_arg["second_key_arg"]}')
async def get_author_of_series_with_cache(
        redis: Redis | None,
        session: AsyncSession,
        series_id: int,
        second_key_arg: str = "author",
):
    return await rel_crud.get_author_of_content(session=session, base_class=models.Series,
                                                base_class_author=models.Series.author, content_id=series_id)
