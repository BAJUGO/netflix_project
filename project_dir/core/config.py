import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()


class JwtSettings(BaseModel):
    private_key: Path = Path(__file__).parent.parent / "certs" / "file-jwt-private.pem"
    public_key: Path = Path(__file__).parent.parent / "certs" / "file-jwt-public.pem"
    algorithm: str = "RS256"
    expire_time_access: timedelta = timedelta(minutes=15)
    expire_time_refresh: timedelta = timedelta(days=7)


class Settings(BaseSettings):
    db_url: str = os.getenv('DB_URL')
    echo: bool = False
    jwt: JwtSettings = JwtSettings()


settings = Settings()
