from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class ReceiptCreate(BaseModel):
    user_id: str
    transaction_date: datetime = datetime.now()

class ReceiptResponse(ReceiptCreate):
    id: str
    total: float