# backend/app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "your-secret-key"
    HST_NUMBER: str = "123456789RT0001"  
    JWT_EXPIRE_MINUTES: int = 1440
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    class Config:
        env_file = ".env"

settings = Settings() 