from fastapi import APIRouter, Depends, HTTPException
from app.services import pdf_generator, qr_code
from app.models.receipt import Receipt
from app.schemas.receipt import ReceiptCreate, ReceiptResponse
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=ReceiptResponse)
async def create_receipt(receipt_data: ReceiptCreate, db=Depends(get_db)):
    # Business logic and validation
    subtotal = sum(item.price * item.quantity for item in receipt_data.items)
    hst = subtotal * 0.13
    total = subtotal + hst
    
    # Generate QR code
    qr_url = qr_code.generate_qr(f"receipt_id:{receipt_data.id}")
    
    # Generate PDF
    business_info = get_business_info(receipt_data.business_id)  # Implement this
    pdf_url = pdf_generator.generate_receipt_pdf(receipt_data.dict(), business_info)
    
    # Save to database
    db_receipt = Receipt(
        id=str(uuid.uuid4()),
        business_id=receipt_data.business_id,
        transaction_date=receipt_data.transaction_date,
        subtotal=subtotal,
        hst=hst,
        total=total,
        items_json=json.dumps([item.dict() for item in receipt_data.items]),
        customer_email=receipt_data.customer_email,
        customer_phone=receipt_data.customer_phone,
        qr_code_url=qr_url,
        pdf_url=pdf_url
    )
    
    db.add(db_receipt)
    db.commit()
    
    # Send notification
    # if receipt_data.customer_email or receipt_data.customer_phone:
    #     send_notification(db_receipt)  # Implement this
    
    return db_receipt