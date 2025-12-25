from datetime import timedelta
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class JwtSettings(BaseModel):
    private_key: Path = Path(__file__).parent.parent / "certs" / "file-jwt-private.pem"
    public_key: Path = Path(__file__).parent.parent / "certs" / "file-jwt-public.pem"
    algorithm: str = "RS256"
    expire_time_minutes: timedelta = timedelta(minutes=15)


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://dima:kiril12AZ@localhost:5432/netflix"
    echo: bool = False
    jwt: JwtSettings = JwtSettings()


settings = Settings()
