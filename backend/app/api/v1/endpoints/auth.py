# app/routers/auth.py
from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from jose import jwt, JWTError, ExpiredSignatureError


from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.config import settings
from app.services.utils import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_token,
    get_user
)

router = APIRouter(tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    # Check if email exists (SQLAlchemy 2.0 style)
    existing = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # If UserCreate.password is SecretStr in your schema, unwrap it:
    password_plain = (
        payload.password.get_secret_value()
        if hasattr(payload.password, "get_secret_value")
        else payload.password
    )

    hashed_password = get_password_hash(password_plain)

    user = User(
        company_name=payload.company_name,
        email=payload.email,
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully"}


@router.post("/login", response_model=Token)
def login_for_access_token(payload: UserLogin, db: Session = Depends(get_db)):
    # Unwrap SecretStr if you use it in the schema
    password_plain = (
        payload.password.get_secret_value()
        if hasattr(payload.password, "get_secret_value")
        else payload.password
    )

    user = authenticate_user(db, payload.email, password_plain)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # Access token (short-lived)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "uid": user.id},
        expires_delta=access_token_expires,
    )

    # Refresh token (longer-lived) — keep in an HttpOnly cookie
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TTL_MIN)
    refresh_token = create_refresh_token(
        data={"sub": user.email, "uid": user.id},
        expires_delta=refresh_token_expires,
    )

    # Return token in body (for API clients) and set refresh cookie for browser flows
    response = JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        status_code=status.HTTP_200_OK,
    )
    # Secure cookie settings — adjust domain/secure flags to your environment
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,          # set False only for local HTTP dev
        samesite="lax",       # or "strict"/"none" (with secure=True)
        max_age=int(refresh_token_expires.total_seconds()),
        expires=int((datetime.now(timezone.utc) + refresh_token_expires).timestamp()),
        path="/",             # you might scope to /auth/refresh
    )
    return response

@router.post("/refresh", response_model=Token)
def refresh_access_token(request: Request):
    """
    Issue a new access token if the refresh_token cookie is valid.
    """
    refresh_cookie = request.cookies.get("refresh_token")
    if not refresh_cookie:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = jwt.decode(
            refresh_cookie,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Mint a new access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": payload.get("sub"), "uid": payload.get("uid")}
    new_access = create_access_token(data=data, expires_delta=access_token_expires)

    return {"access_token": new_access, "token_type": "bearer"}


@router.post("/logout")
def logout(response: Response):
    """
    Clear the refresh_token cookie (log the user out).
    """
    response = JSONResponse(content={"message": "Logged out"}, status_code=200)
    response.delete_cookie("refresh_token", path="/")
    return response

@router.get("/me")
def get_me(
    db: Session = Depends(get_db),
    current_user: Any = Depends(verify_token),  # this is the email from the token
):
    user: User | None = get_user(db, current_user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "company_name": user.company_name,
    }# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdHN0ZWM4MEBnbWFpbC5jb20iLCJ1aWQiOjgsImV4cCI6MTc1NzAzMTM1MCwidHlwZSI6ImFjY2VzcyJ9.5qepgftEj1CZLJI2xp9ODvWOgHR26bWwyOyxmeHxXf0