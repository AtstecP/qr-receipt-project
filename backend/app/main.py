from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import receipts, auth
from app.core.config import settings
from app.middlewear.auth_mw import AutoRefreshMiddleware

app = FastAPI(title="QR Receipt Generator", version="1.0.0")
#app.add_middleware(AutoRefreshMiddleware)
DEV_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://10.0.0.198:5173",   # your LAN Vite URL used on phone
]
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=DEV_ORIGINS, #check it later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(receipts.router, prefix="/api/v1", tags=["receipts"])
#app.include_router(templates.router, prefix="/api/v1/templates", tags=["templates"])