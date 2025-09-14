from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, AnyUrl, Field, StringConstraints
from datetime import datetime

GST_HST_PATTERN = r"^\d{9}(RT\d{4})?$"


class ReceiptTemplateBase(BaseModel):
    logo: Optional[AnyUrl] = None
    gst_hst_number: Annotated[
        str,
        StringConstraints(pattern=GST_HST_PATTERN)
    ] = Field(..., description="9-digit BN, optionally followed by RT0001")

    business_name: Annotated[
        str,
        StringConstraints(min_length=1, max_length=180)
    ]

    contact_phone: Optional[
        Annotated[str, StringConstraints(strip_whitespace=True, max_length=30)]
    ] = None
    contact_email: Optional[EmailStr] = None
    website_url: Optional[AnyUrl] = None


class ReceiptTemplateCreate(ReceiptTemplateBase):
    pass


class ReceiptTemplateUpdate(BaseModel):
    logo: Optional[AnyUrl] = None
    gst_hst_number: Optional[
        Annotated[str, StringConstraints(pattern=GST_HST_PATTERN)]
    ] = None
    business_name: Optional[
        Annotated[str, StringConstraints(min_length=1, max_length=180)]
    ] = None
    contact_phone: Optional[
        Annotated[str, StringConstraints(strip_whitespace=True, max_length=30)]
    ] = None
    contact_email: Optional[EmailStr] = None
    website_url: Optional[AnyUrl] = None


class ReceiptTemplateOut(ReceiptTemplateBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # for Pydantic v2
