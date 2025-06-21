from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session


from app.db.session import get_db
from app.models.user import User
from app.core.config import Settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_access_token(data: dict, expiry_time: timedelta | None = None):
  to_encode = data.copy()
  if expiry_time:
    expire = datetime.utcnow() + expiry_time
  else:
    expire = datetime.utcnow() + timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_TIME)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
  return encoded_jwt


def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user