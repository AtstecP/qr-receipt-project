from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey
from app.db.base import Base

class Receipt(Base):
    __tablename__ = "receipts"
    
    id = Column(String, primary_key=True, index=True)
    business_id = Column(String, ForeignKey("businesses.id"))
    transaction_date = Column(DateTime)
    subtotal = Column(Numeric(10, 2))
    hst = Column(Numeric(10, 2))  # Auto-calculated 13%
    total = Column(Numeric(10, 2))
    items_json = Column(String)  # JSON string of items
    customer_email = Column(String, nullable=True)
    customer_phone = Column(String, nullable=True)
    qr_code_url = Column(String)
    pdf_url = Column(String)