# backend/app/core/security.py
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_jwt_token(data: dict, expires_delta: timedelta) -> str:
    expire = datetime.utcnow() + expires_delta
    return jwt.encode(
        {**data, "exp": expire},
        settings.SECRET_KEY,
        algorithm="HS256"
    )