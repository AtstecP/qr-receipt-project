from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
from backend.app.services.utils import create_access_token, authenticate_user
from app.models.user import User
from app.schemas.user import UserCreate, UserInDB
from app.core.config import settings

router = APIRouter(tags=["auth"])

@router.post("/login")
async def login_for_access_token(user: UserCreate, db: Session = Depends(get_db)):
  if user.email and user.password:
    user = authenticate_user(db, user.email, user.password)
    if user:
      token = create_access_token(data={"sub": user.email})
      refresh_token = create_refresh_token(data={"sub": user.email,
                        "id": user.id})
      response = JSONResponse({"token" : token}, status_code=200)
      response.set_cookie(key="refresh-Token", value=refresh_token)
      return response
  return JSONResponse({"msg": "Invalid Credentials"}, status_code=403)





# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# @router.post("/token", response_model=Token)
# async def login_for_access_token(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     db: Session = Depends(get_db)
# ):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# @router.post("/register", status_code=status.HTTP_201_CREATED)
# async def register_user(
#     user_data: UserCreate,
#     db: Session = Depends(get_db)
# ):
#     # if alredy registered
#     db_user = get_user(db, user_data.email)
#     if db_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email already registered"
#         )
    
#     # createing new user
#     hashed_password = get_password_hash(user_data.password)
#     user = User(
#         email=user_data.email,
#         hashed_password=hashed_password,
#         full_name=user_data.full_name,
#         is_active=True
#     )
#     db.add(user)
#     db.commit()
#     return {"message": "User created successfully"}

# # Dependnenciees for endpoints
# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         token_data = TokenData(email=email)
#     except JWTError:
#         raise credentials_exception
    
#     user = get_user(db, email=token_data.email)
#     if user is None:
#         raise credentials_exception
#     return user

# async def get_current_active_user(
#     current_user: User = Depends(get_current_user)
# ):
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user