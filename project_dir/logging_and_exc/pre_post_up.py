from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from redis.asyncio import Redis

from project_dir.core import settings


def log_info(data, where_to_load: str):
    with open(
        f"D:/project_db_auth/project_dir/logging_and_exc/{where_to_load}", "a"
    ) as file:
        file.write(data)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log_info(
        data="\n$$$$$  application has been started\n", where_to_load="log_file.txt"
    )
    redis_client = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
        username=settings.redis.username,
        password=settings.redis.password,
        decode_responses=True,
    )
    app.state.redis = redis_client

    try:
        yield
    finally:
        log_info(
            data="\n$$$$$  application has been stopped\n", where_to_load="log_file.txt"
        )
        await redis_client.aclose()


async def get_redis(request: Request) -> Redis:
    return request.app.state.redis
