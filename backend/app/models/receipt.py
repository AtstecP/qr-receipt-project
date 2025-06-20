from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from app.db.base import Base

class Receipt(Base):
    __tablename__ = "receipts"
    
    id = Column(String, primary_key=True, index=True)
    receipt_id = Column(Numeric(10, 2))
    user_id = Column(String, ForeignKey("user.id"))
    transaction_date = Column(DateTime)
    total = Column(Numeric(10, 2))