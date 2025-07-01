from datetime import datetime
from pydantic import BaseModel



class ReceiptCreate(BaseModel):
    total : float
    transaction_date: datetime = datetime.now()

class ReceiptResponse(ReceiptCreate):
    pdf_endpoint: str