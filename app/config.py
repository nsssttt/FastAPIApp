from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Hotel Management System"
    app_version: str = "1.0.0"

    database_url: str = "postgresql://hotel_user:hotel_pass@db:5432/hotel_db"

    cors_origins: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
