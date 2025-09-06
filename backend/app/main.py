from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.v1.endpoints import receipts, auth
from app.core.config import settings
from app.middlewear.auth_mw import AutoRefreshMiddleware

app = FastAPI(
    title="QR Receipt Generator",
    version="1.0.0", 
    swagger_ui_parameters={"persistAuthorization": True},)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description="API for QR receipts",
        routes=app.routes,
    )

    # Declare HTTP Bearer (JWT) scheme
    schema.setdefault("components", {}).setdefault("securitySchemes", {})
    schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    # Apply this security to ALL operations (or add per-route if you prefer)
    for path in schema.get("paths", {}).values():
        for op in path.values():
            op.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi


DEV_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://10.0.0.198:5173",  
]
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=DEV_ORIGINS, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(receipts.router, prefix="/api/v1", tags=["receipts"])
# app.include_router(templates.router, prefix="/api/v1/templates", tags=["templates"])
# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload