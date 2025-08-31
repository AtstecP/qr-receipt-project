# app/schemas/common.py (optional place for shared imports/types)
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, EmailStr, SecretStr


# --- Receipts ---

class ReceiptBase(BaseModel):
    total: Decimal = Field(ge=0)
    transaction_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    # if you might populate by field name when using aliases later
    model_config = ConfigDict(
        str_strip_whitespace=True,     # trims incoming strings
        populate_by_name=True,
    )


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptResponse(ReceiptBase):
    pdf_endpoint: str
    # If you return ORM rows directly from FastAPI:
    model_config = ConfigDict(
        from_attributes=True,          # replaces v1's orm_mode=True
        str_strip_whitespace=True,
        populate_by_name=True,
    )
