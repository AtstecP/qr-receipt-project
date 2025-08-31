# app/middleware/auto_refresh.py
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.services.utils import create_access_token

# Optional: if you *also* want to mirror the new access token into a non-HttpOnly cookie.
ISSUE_ACCESS_COOKIE = False  # recommended: keep False; frontend uses Authorization header


def _decode(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        return None
    except JWTError:
        # structurally invalid / wrong signature
        raise


class AutoRefreshMiddleware(BaseHTTPMiddleware):
    """
    - Accepts access token from Authorization header: 'Bearer <jwt>'
    - If missing/expired and refresh_token cookie is valid, mints a new access token
      and attaches it to the response via the 'X-New-Access-Token' header (and optionally a cookie).
    - Sets request.state.user_payload for downstream handlers if available.
    """

    async def dispatch(self, request: Request, call_next):
        # 1) Try Authorization header
        auth_header = request.headers.get("Authorization", "")
        access_token = None
        if auth_header.lower().startswith("bearer "):
            access_token = auth_header.split(" ", 1)[1].strip()

        payload = None
        if access_token:
            try:
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            except ExpiredSignatureError:
                payload = None  # attempt refresh below
            except JWTError:
                return JSONResponse({"detail": "Invalid access token"}, status_code=401)

        # 2) If we have a good payload, attach & proceed
        if payload:
            request.state.user_payload = payload  # contains 'sub', maybe 'uid' etc.
            return await call_next(request)

        # 3) Try refresh cookie
        refresh_cookie = request.cookies.get("refresh_token")
        if not refresh_cookie:
            return JSONResponse({"detail": "Token required"}, status_code=401)

        try:
            r_payload = jwt.decode(refresh_cookie, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except ExpiredSignatureError:
            return JSONResponse({"detail": "Refresh token expired"}, status_code=401)
        except JWTError:
            return JSONResponse({"detail": "Invalid refresh token"}, status_code=401)

        # 4) Mint a new access token (keep the same subject/user info)
        # Include both sub and uid if present in refresh payload.
        new_data = {}
        if "sub" in r_payload:
            new_data["sub"] = r_payload["sub"]
        if "uid" in r_payload:
            new_data["uid"] = r_payload["uid"]

        # (Optionally) pass a custom expiry; otherwise utils will use settings.ACCESS_TOKEN_EXPIRE_MINUTES
        new_access = create_access_token(new_data)

        # Attach the user for this request so downstream handlers see an authenticated user
        try:
            request.state.user_payload = jwt.decode(new_access, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        except JWTError:
            # Extremely unlikely right after encoding; fail closed.
            return JSONResponse({"detail": "Could not issue access token"}, status_code=401)

        # 5) Call the app and then attach headers/cookies on the way out
        response = await call_next(request)

        # Let the frontend capture the new token (axios interceptor) and store it
        response.headers["X-New-Access-Token"] = new_access

        if ISSUE_ACCESS_COOKIE:
            # Non-HttpOnly mirror for convenience (not recommended for security).
            response.set_cookie(
                key="access",
                value=new_access,
                httponly=False,  # JS-readable; set True if you want cookie-only auth
                secure=False,    # True when HTTPS
                samesite="Lax",
                max_age=int(timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds()),
                expires=int((datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()),
                path="/",
            )

        return response
