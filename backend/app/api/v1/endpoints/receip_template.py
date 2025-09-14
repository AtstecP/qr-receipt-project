from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.responses import FileResponse

from app.db.session import get_db
from app.models.receipt_template import ReceiptTemplate
from app.schemas.receip_template import (
    ReceiptTemplateCreate,
    ReceiptTemplateUpdate,
    ReceiptTemplateOut,
)
from app.services.utils import verify_token, get_user_id
from app.services.receipts.pdf_generator import generate_template_pdf

router = APIRouter(prefix="/receip_template", tags=["receip_template"])


def _get_user_template_or_none(db: Session, user_id: int) -> ReceiptTemplate | None:
    return db.execute(
        select(ReceiptTemplate).where(ReceiptTemplate.user_id == user_id)
    ).scalar_one_or_none()


@router.get("/", response_model=ReceiptTemplateOut)
def get_receipt_template(
    db: Session = Depends(get_db),
    current_user=Depends(verify_token),
):
    """
    Get the receipt template for the current user.

    - **404** if no template exists for this user.
    - Returns all template fields, including `id`, `user_id`, and timestamps.
    """
    user_id = get_user_id(current_user)
    tpl = _get_user_template_or_none(db, user_id)
    if not tpl:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found for this user.",
        )
    return tpl


@router.post("/", response_model=ReceiptTemplateOut, status_code=status.HTTP_201_CREATED)
def create_receipt_template(
    payload: ReceiptTemplateCreate,
    db: Session = Depends(get_db),
    current_user=Depends(verify_token),
):
    """
    Create a receipt template for the current user.

    - Each user can only have **one template**.
    - Returns **409** if the user already has a template.
    - Persists the template and returns the saved record.
    """
    user_id = get_user_id(current_user)
    existing = _get_user_template_or_none(db, user_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already has a template. Use PATCH to update it.",
        )

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
    db.commit()
    db.refresh(tpl)
    return tpl


@router.patch("/", response_model=ReceiptTemplateOut)
def update_receipt_template(
    payload: ReceiptTemplateUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(verify_token),
):
    """
    Update the receipt template for the current user.

    - Only the fields provided in the request body are updated.
    - **404** if no template exists for this user.
    - Returns the updated template record.
    """
    user_id = get_user_id(current_user)
    tpl = _get_user_template_or_none(db, user_id)
    if not tpl:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found for this user.",
        )

    if payload.logo is not None:
        tpl.logo = str(payload.logo)
    if payload.gst_hst_number is not None:
        tpl.gst_hst_number = payload.gst_hst_number
    if payload.business_name is not None:
        tpl.business_name = payload.business_name
    if payload.contact_phone is not None:
        tpl.contact_phone = payload.contact_phone
    if payload.contact_email is not None:
        tpl.contact_email = str(payload.contact_email)
    if payload.website_url is not None:
        tpl.website_url = str(payload.website_url)

    db.add(tpl)
    db.commit()
    db.refresh(tpl)
    return tpl


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_receipt_template(
    db: Session = Depends(get_db),
    current_user=Depends(verify_token),
):
    """
    Delete the receipt template for the current user.

    - Does nothing if no template exists.
    - Always returns **204 No Content** on success.
    """
    user_id = get_user_id(current_user)
    tpl = _get_user_template_or_none(db, user_id)
    if not tpl:
        return
    db.delete(tpl)
    db.commit()

@router.get("/pdf/temaplte", response_class=FileResponse, status_code=status.HTTP_200_OK)
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
