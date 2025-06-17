from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import receipts, templates, auth
from app.core.config import settings

app = FastAPI(title="QR Receipt Generator", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(receipts.router, prefix="/api/v1/receipts", tags=["receipts"])
app.include_router(templates.router, prefix="/api/v1/templates", tags=["templates"])