from datetime import datetime, timedelta
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt

from app.core.config import settings 
from app.services.utils import create_access_token

class AutoRefreshMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        access  = request.cookies.get("access")
        refresh = request.cookies.get("refresh")

        if not access:
            return await self._fail_or_refresh(request, call_next, refresh)


        try:
            payload = jwt.decode(access, settings.SECRET, algorithms=[settings.ALGORITHM])
            request.state.user = payload["sub"]
            return await call_next(request)

        except jwt.ExpiredSignatureError:

            return await self._fail_or_refresh(request, call_next, refresh)

        except jwt.InvalidTokenError:
            return JSONResponse({"detail": "Invalid access"}, 401)

    async def _fail_or_refresh(self, request, call_next, refresh_cookie):
        if not refresh_cookie:
            return JSONResponse({"detail": "Token required"}, 401)

        try:
            r_payload = jwt.decode(refresh_cookie, settings.SECRET, algorithms=[settings.ALGORITHM])
        except jwt.ExpiredSignatureError:
            return JSONResponse({"detail": "Refresh expired"}, 401)
        except jwt.InvalidTokenError:
            return JSONResponse({"detail": "Invalid refresh"}, 401)

   


        new_access  = create_access_token(r_payload["sub"])
        # new_refresh = _create_refresh(r_payload["sub"])  

        response = await call_next(request)
        response.set_cookie(
            key="access", value=new_access,
            httponly=True, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60,
            samesite="Strict", secure=True
        )
        # response.set_cookie("refresh", new_refresh, …)  
        return response
