from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.responses import FileResponse
from fastapi import (
    APIRouter, 
    Depends, 
    HTTPException, 
    status, 
    UploadFile, 
    File, 
    Form, 
    Request
    )

from pydantic import ValidationError
from pathlib import Path
from uuid import uuid4
from typing import Any, Optional

from app.db.session import get_db
from app.models.receipt_template import ReceiptTemplate
from app.schemas.receip_template import ReceiptTemplateForm, ReceiptTemplateOut
from app.services.utils import verify_token, get_user_id
from app.services.receipts.pdf_generator import generate_template_pdf

router = APIRouter(prefix="/receip_template", tags=["receip_template"])

LOGO_DIR = Path("app/static/logo")
ALLOWED_TYPES = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
    "image/svg+xml": ".svg",
}
MAX_BYTES = 4 * 1024 * 1024  



def _get_user_template_or_none(db: Session, user_id: int) -> ReceiptTemplate | None:
    return db.execute(
        select(ReceiptTemplate).where(ReceiptTemplate.user_id == user_id)
    ).scalar_one_or_none()


@router.get("/preview", response_class=FileResponse, status_code=status.HTTP_200_OK)
def preview_template_pdf(
    db: Session = Depends(get_db),
    current_user=Depends(verify_token),
):
    """
    Generate and return a PDF preview rendered from the user's ReceiptTemplate.
    Does not create a Receipt row.
    """


    path = generate_template_pdf(db, current_user)
    return FileResponse(
        path, 
        media_type="application/pdf", 
        filename=f"template_preview_{current_user}.pdf")


@router.post("/form", response_model=ReceiptTemplateOut, status_code=status.HTTP_200_OK)
async def create_or_update_template_via_form(
    request: Request,
    form: ReceiptTemplateForm = Depends(ReceiptTemplateForm.as_form),
    db: Session = Depends(get_db),
    current_user: Any = Depends(verify_token),
):
    user_id = get_user_id(db, current_user)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # 1) Save the file if provided and build a public URL
    final_logo_url = None
    if form.logo_file:
        if form.logo_file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="Invalid file type")
        content = await form.logo_file.read(MAX_BYTES + 1)
        if len(content) > MAX_BYTES:
            raise HTTPException(status_code=413, detail="File too large (max 2MB)")

        LOGO_DIR.mkdir(parents=True, exist_ok=True)
        ext = ALLOWED_TYPES[form.logo_file.content_type]
        fname = f"user_{user_id}_{uuid4().hex}{ext}"
        fpath = LOGO_DIR / fname
        with open(fpath, "wb") as f:
            f.write(content)

        base = str(request.base_url).rstrip("/")
        final_logo_url = f"{base}/static/logo/{fname}"
    else:
        final_logo_url = str(form.logo_url) if form.logo_url else None

    # 2) Validate + map to your create schema
    payload = form.to_create(final_logo_url)

    # 3) Create-or-update the single template
    existing = _get_user_template_or_none(db, user_id)
    if existing is None:
        tpl = ReceiptTemplate(
            user_id=user_id,
            logo=str(payload.logo) if payload.logo else None,
            gst_hst_number=payload.gst_hst_number,
            business_name=payload.business_name,
            contact_phone=payload.contact_phone,
            contact_email=str(payload.contact_email) if payload.contact_email else None,
            website_url=str(payload.website_url) if payload.website_url else None,
        )
        db.add(tpl)
    else:
        tpl = existing
        if payload.logo is not None:
            tpl.logo = str(payload.logo)
        tpl.gst_hst_number = payload.gst_hst_number
        tpl.business_name = payload.business_name
        tpl.contact_phone = payload.contact_phone
        tpl.contact_email = str(payload.contact_email) if payload.contact_email else None
        tpl.website_url = str(payload.website_url) if payload.website_url else None

    db.commit()
    db.refresh(tpl)
    return tpl
