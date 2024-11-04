import os
from typing import List

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_PORT: int
    POSTGRES_HOSTNAME: str
    DATABASE_DIALECT: str
    
    jwt_algorithm: str
    secret_key: str
    access_token_lifetime: int

    kinopoisk_api_key: str
    
    class Config:
        env_file = os.getenv("ENV_FILE")
        env_file_encoding = "utf-8"
        

def get_settings() -> Settings:
    """Функция для получения настроек в зависимости от среды."""
    settings = Settings()
    return settings


env = get_settings()
