from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.db.base import Base

class ReceiptTemplate(Base):
    __tablename__ = "receipt_templates"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    logo = Column(Text, nullable=True)                 
    gst_hst_number = Column(String(15), nullable=False) 
    business_name = Column(String(180), nullable=False)
    contact_phone = Column(String(30), nullable=True)
    contact_email = Column(String(254), nullable=True)
    website_url = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
