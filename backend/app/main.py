from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import receipts, auth
from app.core.config import settings
from app.middlewear.auth_mw import AutoRefreshMiddleware

app = FastAPI(title="QR Receipt Generator", version="1.0.0")
#app.add_middleware(AutoRefreshMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(receipts.router, prefix="/api/v1/receipts", tags=["receipts"])
#app.include_router(templates.router, prefix="/api/v1/templates", tags=["templates"])