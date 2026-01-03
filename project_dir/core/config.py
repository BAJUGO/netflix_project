import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()


class JwtSettings(BaseModel):
    private_key: Path = os.getenv('PRIVATE_KEY')
    public_key: str = os.getenv('PUBLIC_KEY')
    algorithm: str = "RS256"
    expire_time_access: timedelta = timedelta(minutes=15)
    expire_time_refresh: timedelta = timedelta(days=7)


class Settings(BaseSettings):
    db_url: str = os.getenv('DB_URL')
    echo: bool = True
    jwt: JwtSettings = JwtSettings()


settings = Settings()
