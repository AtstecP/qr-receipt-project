# app/services/utils.py
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List

from fastapi import Header, HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy import select, func, desc, and_
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.models.receipt import Receipt


# ---- password hashing (prefer argon2; fallback to bcrypt) ----
def _build_pwd_context() -> CryptContext:
    try:
        # Prefer argon2 if installed
        return CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
    except Exception:
        # Fallback to bcrypt-only if argon2 unavailable
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

pwd_context = _build_pwd_context()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# ---- user lookups ----
def get_user(db: Session, email: str) -> Optional[User]:
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

def get_user_id(db: Session, email: str) -> Optional[int]:
    row = db.execute(select(User.id).where(User.email == email)).first()
    return row[0] if row else None

def get_company_name(db: Session, id: int) -> Optional[str]:
    row = db.execute(select(User.company_name).where(User.id == id)).first()
    return row[0] if row else None


# ---- JWT helpers ----
def _expiry_from_delta(expires_delta: Optional[timedelta], fallback_minutes: int) -> datetime:
    if isinstance(expires_delta, timedelta):
        return datetime.now(timezone.utc) + expires_delta
    return datetime.now(timezone.utc) + timedelta(minutes=fallback_minutes)

def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = _expiry_from_delta(expires_delta, settings.REFRESH_TTL_MIN)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = _expiry_from_delta(expires_delta, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ---- auth dependency (reads Authorization header) ----
def verify_token(authorization: Optional[str] = Header(None)) -> str:
    """
    Reads 'Authorization: Bearer <jwt>' and returns the user's email (sub).
    Raise 401 if missing/invalid.
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token = authorization.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token payload invalid")
        return username  # email string
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# ---- stats for Dashboard (matches your frontend expectations) ----
def get_user_stats(db: Session, email: str) -> Dict[str, Any]:
    """
    Returns:
      - total: sum of all receipts for user
      - total_today: sum of today's receipts for user (UTC day)
      - receipts_count: total count for user
      - recent_receipts: last 10 receipts [{total, transaction_date}]
    """
    uid = get_user_id(db, email)
    if uid is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user_id_str = str(uid)

    # Total & count
    total_sum, count = db.execute(
        select(func.coalesce(func.sum(Receipt.total), 0), func.count(Receipt.id))
        .where(Receipt.user_id == user_id_str)
    ).one()

    # Today's totals (UTC day window)
    now = datetime.now(timezone.utc)
    start = datetime(now.year, now.month, now.day, tzinfo=timezone.utc)
    end = start + timedelta(days=1)

    total_today = db.execute(
        select(func.coalesce(func.sum(Receipt.total), 0))
        .where(and_(Receipt.user_id == user_id_str,
                    Receipt.transaction_date >= start,
                    Receipt.transaction_date < end))
    ).scalar_one()

    # Recent receipts (last 10)
    rows: List[tuple] = db.execute(
        select(Receipt.total, Receipt.transaction_date)
        .where(Receipt.user_id == user_id_str)
        .order_by(desc(Receipt.transaction_date))
        .limit(10)
    ).all()

    recent = [
        {"total": row[0], "transaction_date": row[1]}
        for row in rows
    ]

    return {
        "user_id": uid,
        "total": total_sum,                # Decimal; FastAPI will serialize
        "total_today": total_today,        # Decimal
        "receipts_count": int(count),
        "recent_receipts": recent,
    }
