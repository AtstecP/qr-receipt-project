from pdfkit import from_string
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy.orm import Session

import os
from datetime import datetime
from typing import Any, Dict, Optional

from app.core.config import settings
from app.services.utils import get_company_name, get_user_id
from app.models.receipt import Receipt
from app.models.receipt_template import ReceiptTemplate




CWD = os.getcwd()
TEMPLATE_DIR = os.path.join(CWD, "app", "services", "receipts", "jinja_templates")
TEMP_DIR = os.path.join(CWD, "app", "services", "receipts", "temporary_files")

os.makedirs(TEMP_DIR, exist_ok=True)


ENV = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
    enable_async=False,
)

def _pdfkit_config():
    """
    Use a custom wkhtmltopdf path when set in .env:
      WKHTMLTOPDF_CMD="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
    """
    cmd = getattr(settings, "WKHTMLTOPDF_CMD", None)
    if not cmd:
        return None
    try:
        import pdfkit
        return pdfkit.configuration(wkhtmltopdf=cmd)
    except Exception:
        return None

PDFKIT_CONFIG = _pdfkit_config()

def model_to_dict(obj) -> Dict[str, Any]:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}  # type: ignore[attr-defined]



def generate_receipt_pdf(db: Session, recipt_id: str) -> str:
    """
    Render a receipt PDF from DB using Jinja + pdfkit, save it, and return the file path.
    If the PDF already exists, returns the existing file path.
    """
    file_path = os.path.join(TEMP_DIR, f"{recipt_id}.pdf")
    if os.path.exists(file_path):
        return file_path

    # Load template
    try:
        template = ENV.get_template("receipt.html")
    except Exception as e:
        raise RuntimeError(f"Template 'receipt.html' load error: {e}")

    # Fetch receipt row
    receipt: Optional[Receipt] = db.query(Receipt).filter(Receipt.receipt_id == recipt_id).first()
    if not receipt:
        raise RuntimeError(f"Receipt '{recipt_id}' not found")

    # Build render context
    ctx: Dict[str, Any] = {
        **model_to_dict(receipt),
        "company_name": get_company_name(db, receipt.user_id),
    }

    # Render to HTML
    html = template.render(ctx)

    # Convert HTML -> PDF bytes
    try:
        pdf_bytes = from_string(html, options={"encoding": "UTF-8"}, configuration=PDFKIT_CONFIG)
    except Exception as e:
        raise RuntimeError(f"PDF render failed: {e}")

    # Write PDF to disk
    try:
        with open(file_path, "wb") as f:
            f.write(pdf_bytes)
    except Exception as e:
        raise RuntimeError(f"Saving PDF failed: {e}")

    return file_path


def generate_template_pdf(db: Session, email: str) -> str:
    """
    Render a **preview** PDF using the user's ReceiptTemplate (no DB Receipt row).
    Always regenerates so changes show immediately.
    """
    # Resolve user_id from email
    user_id = get_user_id(db, email)
    if not user_id:
        raise RuntimeError("User not found or unauthorized")

    out_path = os.path.join(TEMP_DIR, f"template_preview_{email}.pdf")

    # Load template
    try:
        template = ENV.get_template("receipt.html")
    except Exception as e:
        raise RuntimeError(f"Template 'receipt.html' load error: {e}")

    # Load the user's template header fields
    tpl: Optional[ReceiptTemplate] = (
        db.query(ReceiptTemplate).filter(ReceiptTemplate.user_id == user_id).first()
    )
    if not tpl:
        raise RuntimeError(f"No ReceiptTemplate found for user {user_id}")

    # Minimal preview context (no items in your receipts)
    ctx: Dict[str, Any] = {
        "receipt_id": "PREVIEW-ONLY",
        "transaction_date": datetime.utcnow(),
        "total": 42.00,  # sample total

        # Header fields from the user's template:
        "business_name": tpl.business_name,
        "logo": tpl.logo,
        "gst_hst_number": tpl.gst_hst_number,
        "contact_phone": tpl.contact_phone,
        "contact_email": tpl.contact_email,
        "website_url": tpl.website_url,
    }

    # Render HTML
    html = template.render(ctx)

    # Convert to PDF
    try:
        pdf_bytes = from_string(html, options={"encoding": "UTF-8"}, configuration=PDFKIT_CONFIG)
    except Exception as e:
        raise RuntimeError(f"Preview PDF render failed: {e}")

    # Save to disk (always overwrite preview)
    try:
        with open(out_path, "wb") as f:
            f.write(pdf_bytes)
    except Exception as e:
        raise RuntimeError(f"Saving preview PDF failed: {e}")

    return out_path
