# backend/app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "your-secret-key"
    HST_NUMBER: str = "123456789RT0001"
    REFRESH_TTL_MIN: int = 1440
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    BASE_URL: str = "http://10.0.0.198:8000"

    # replaces inner class Config in v1
    model_config = SettingsConfigDict(
        env_file=".env",      # load variables from .env
        extra="ignore",       # ignore unexpected env vars
    )


settings = Settings()