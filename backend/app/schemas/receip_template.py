from typing import Optional, Annotated
from datetime import datetime
from pydantic import BaseModel, EmailStr, AnyUrl, Field, StringConstraints
from pydantic import ConfigDict

# 👇 ONLY needed for the form binder
from fastapi import Form, File, UploadFile

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
        from_attributes = True  # Pydantic v2


# -------------------------------------------------------------------
# 🌟 Form binder: receive multipart/form-data (incl. optional file)
# -------------------------------------------------------------------
class ReceiptTemplateForm(BaseModel):
    """
    Helper model to bind a multipart/form-data form:
    - Accepts an optional file: `logo_file`
    - Or a plain URL: `logo_url`
    - Plus the rest of the template fields
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # file OR url (file wins if provided)
    logo_file: UploadFile | None = None

    gst_hst_number: Annotated[str, StringConstraints(pattern=GST_HST_PATTERN)]
    business_name: Annotated[str, StringConstraints(min_length=1, max_length=180)]
    contact_phone: Optional[Annotated[str, StringConstraints(strip_whitespace=True, max_length=30)]] = None
    contact_email: Optional[EmailStr] = None
    website_url: Optional[AnyUrl] = None

    @classmethod
    def as_form(
        cls,
        logo_file: UploadFile | None = File(None),
        gst_hst_number: Optional[str] = Form(None),
        business_name: Optional[str] = Form(None),
        contact_phone: Optional[str] = Form(None),
        contact_email: Optional[EmailStr] = Form(None),
        website_url: Optional[AnyUrl] = Form(None),
    ) -> "ReceiptTemplateForm":
        return cls(
            logo_file=logo_file,
            gst_hst_number=gst_hst_number,
            business_name=business_name,
            contact_phone=contact_phone,
            contact_email=contact_email,
            website_url=website_url,
        )

    def to_create(self, final_logo_url: Optional[str]) -> ReceiptTemplateCreate:
        """
        Convert the bound form to your existing ReceiptTemplateCreate,
        using the logo URL resolved by the endpoint (uploaded file or logo_url).
        """
        return ReceiptTemplateCreate.model_validate({
            "logo": final_logo_url or self.logo_url,
            "gst_hst_number": self.gst_hst_number,
            "business_name": self.business_name,
            "contact_phone": self.contact_phone,
            "contact_email": self.contact_email,
            "website_url": self.website_url,
        })
