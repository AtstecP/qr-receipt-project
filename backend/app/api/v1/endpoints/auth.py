from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from app.services.utils import get_password_hash, authenticate_user, create_access_token, create_refresh_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.config import settings

router = APIRouter(tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = get_password_hash(user.password)
    user = User(
        company_name = user.company_name,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}



@router.post("/login")
async def login_for_access_token(user: UserLogin, db: Session = Depends(get_db)):
  if user.email and user.password:
    user = authenticate_user(db, user.email, user.password)
    if user:
      token = create_access_token(data={"sub": user.email})
      refresh_token = create_refresh_token(data={"sub": user.email,"id": user.id})
      response = JSONResponse({"token" : token}, status_code=200)
      response.set_cookie(key="token", value=token)
      return response
  return JSONResponse({"msg": "Invalid Credentials"}, status_code=403)
