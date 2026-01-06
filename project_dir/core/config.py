from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()


class RedisSettings(BaseModel):
    host: str
    port: int
    db: int
    username: str
    password: str


class JwtSettings(BaseModel):
    private_key: Path
    public_key: Path
    algorithm: str
    expire_time_access: timedelta = timedelta(minutes=15)
    expire_time_refresh: timedelta = timedelta(days=7)


class Settings(BaseSettings):
    db_url: str
    echo: bool = True
    jwt: JwtSettings
    redis: RedisSettings

    class Config:
        env_nested_delimiter = "__"


settings = Settings()
