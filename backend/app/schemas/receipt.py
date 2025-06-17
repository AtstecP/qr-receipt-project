from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class ReceiptItem(BaseModel):
    description: str
    quantity: int
    price: float

class ReceiptCreate(BaseModel):
    business_id: str
    transaction_date: datetime = datetime.now()
    items: List[ReceiptItem]
    customer_email: Optional[str] = None
    customer_phone: Optional[str] = None

class ReceiptResponse(ReceiptCreate):
    id: str
    subtotal: float
    hst: float
    total: float
    qr_code_url: str
    pdf_url: str