from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://dima:kiril12AZ@localhost:5432/netflix"
    echo: bool = True


settings = Settings()
