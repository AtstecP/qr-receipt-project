from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID  

import uuid
from app.db.base import Base

class Receipt(Base):
    __tablename__ = "receipts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    receipt_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    transaction_date = Column(DateTime(timezone=True))
    total = Column(Numeric(10, 2))