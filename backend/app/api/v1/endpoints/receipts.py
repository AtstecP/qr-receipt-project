from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.services import pdf_generator, qr_code
from app.models.receipt import Receipt
from app.schemas.receipt import ReceiptCreate, ReceiptResponse
from app.db.session import get_db
from app.services.qr_code import generate_qr

router = APIRouter()

# @router.get("/qr")
# async def get_qr():
#     file_name = generate_qr('http://192.168.0.144:8000/api/v1/receipts/pdf')
#     return FileResponse(f'{file_name}')

# @router.get("/pdf")
# async def get_qr():
#     return FileResponse('app/services/your_pdf_file_here.pdf')

@router.post("/", response_model=ReceiptResponse)
async def create_receipt(receipt_data: ReceiptCreate, db=Depends(get_db)):

    # Generate PDF
    business_info = get_business_info(receipt_data.business_id)  # Implement this
    pdf_url = pdf_generator.generate_receipt_pdf(receipt_data.dict(), business_info)
    
    # Save to database
    db_receipt = Receipt(
        id=str(uuid.uuid4()),
        business_id=receipt_data.user_id,
        transaction_date=receipt_data.transaction_date,
        total=receipt_data.total,
    )
    
    db.add(db_receipt)
    db.commit()
    
    # Send notification
    # if receipt_data.customer_email or receipt_data.customer_phone:
    #     send_notification(db_receipt)  # Implement this
    
    return db_receipt