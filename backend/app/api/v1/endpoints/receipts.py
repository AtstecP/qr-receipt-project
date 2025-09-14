from __future__ import annotations
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.receipt import Receipt
from app.schemas.receipt import ReceiptCreate, ReceiptResponse
from app.services.utils import verify_token, get_user_id
from app.services.receipts.qr_code import generate_qr
from app.services.receipts.pdf_generator import generate_receipt_pdf
from app.core.config import settings

from app.services.receipts.utils import get_user_stats, get_receipts

router = APIRouter(prefix="/receipts", tags=["receipts"])


@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    current_user: Any = Depends(verify_token),
):
    
    return get_user_stats(db, current_user)


@router.get("/all")
def get_stats(
    db: Session = Depends(get_db),
    current_user: Any = Depends(verify_token),
):
    return get_receipts(db, current_user)


@router.get("/pdf/{receipt_id}")
def get_pdf(receipt_id: UUID, db: Session = Depends(get_db)):
    """
    Stream the generated PDF for a given receipt UUID.
    """
    path = generate_receipt_pdf(db, str(receipt_id))
    return FileResponse(path, media_type="application/pdf", filename=f"{receipt_id}.pdf")



@router.post("/", response_model=ReceiptResponse, status_code=status.HTTP_201_CREATED)
def create_receipt(
    receipt_data: ReceiptCreate,
    db: Session = Depends(get_db),
    current_user: Any = Depends(verify_token),
):
    """
    Create a receipt row, persist it, generate a QR that points to the PDF endpoint,
    and return fields matching ReceiptResponse.
    """
    # Resolve current user → DB id
    user_id = get_user_id(db, current_user)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    # Generate UUID in Python to store in receipt_id (SQLAlchemy column uses UUID type)
    rid = uuid4()

    row = Receipt(
        receipt_id=rid,
        user_id=str(user_id),
        transaction_date=receipt_data.transaction_date,
        total=Decimal(receipt_data.total),  
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    # Build a public URL for the PDF endpoint (avoid hard-coding LAN IPs)
    # Add BASE_URL="http://localhost:8000" (or prod URL) to your .env and Settings
    base = getattr(settings, "BASE_URL", "http://localhost:8000")
    pdf_url = f"{base}/api/v1/receipts/pdf/{row.receipt_id}"

    # Generate a QR image (your function likely returns a file path or a data URL)
    pdf_endpoint = generate_qr(pdf_url)

    # Return data that matches ReceiptResponse (pdf_endpoint + receipt fields)
    return {
        "pdf_endpoint": pdf_endpoint,
        "total": row.total,  # Decimal will serialize fine
        "transaction_date": row.transaction_date,
    }
