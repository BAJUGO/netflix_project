from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis

from project_dir.core import settings


def log_info(data, where_to_load: str):
    with open(f"D:/project_db_auth/project_dir/loging_and_exc/{where_to_load}", "a") as file:
        file.write(data)


redis_client: Redis | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    log_info(
        data="\n$$$$$  application has been started\n", where_to_load="log_file.txt"
    )
    global redis_client
    redis_client = Redis(host=settings.redis.host, port=settings.redis.port, db=settings.redis.db,
                         decode_responses=True)

    yield
    log_info(
        data="\n$$$$$  application has been stopped\n", where_to_load="log_file.txt"
    )
    await redis_client.aclose()


async def get_redis() -> Redis:
    return redis_client
