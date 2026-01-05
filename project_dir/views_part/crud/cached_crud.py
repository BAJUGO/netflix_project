import json
from functools import wraps

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from project_dir.models import Author
from project_dir.views_part.crud.crud import getter_by_id_session
from project_dir.views_part.crud.relationship_crud import get_author_series_session
import project_dir.views_part.schemas as schemas


def cache_response_wrapper(ttl: int, namespace: str, key_arg: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{namespace}:{kwargs.get(key_arg)}"

            if not (cache := kwargs.get('redis')):
                return await func(*args, **kwargs)

            if cached_value := await cache.get(cache_key):
                return json.loads(cached_value)

            response = await func(*args, **kwargs)
            try:
                await cache.set(name=cache_key, value=json.dumps(response), ex=ttl)
            except Exception as e:
                print(f"Couldn't cache this shit! {e}")
            return response

        return wrapper

    return decorator


@cache_response_wrapper(ttl=15, namespace="authors", key_arg="author_id")
async def get_author_with_cache(author_id: int, redis: Redis | None, session: AsyncSession):
    author = await getter_by_id_session(session, Author, author_id)
    return schemas.AuthorSchema.model_validate(author).model_dump()


@cache_response_wrapper(ttl=30, namespace="authors", key_arg="series")
async def get_authors_series_with_cache(redis: Redis | None, session: AsyncSession, series: str = "series"):
    return await get_author_series_session(session)