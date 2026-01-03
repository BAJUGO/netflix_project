import json

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from project_dir.views_part.crud import T, getter_by_id_session
from project_dir.views_part.schemas import AuthorSchema


async def cache_object_with_id(rd: Redis, session: AsyncSession, obj_id: int, orm_model: type[T], ex: int = 30):
    cached_key = f"str{orm_model}:{obj_id}"
    cached_object = await rd.get(cached_key)
    if cached_object:
        return json.loads(cached_object)
    else:
        obj = await getter_by_id_session(session, orm_model, obj_id)
        await rd.set(name=cached_key, value=AuthorSchema.model_validate(obj).model_dump_json(), ex=ex)
        return obj