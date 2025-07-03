from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

from app.services.utils import verify_token, get_user_id
from app.services.recipts.utils import generate_uuid
from app.models.receipt import Receipt
from app.models.user import User
from app.schemas.receipt import ReceiptCreate, ReceiptResponse
from app.db.session import get_db
from app.services.recipts.qr_code import generate_qr
from app.services.recipts.pdf_generator import generate_receipt_pdf
router = APIRouter()

# @router.get("/qr")
# async def get_qr():
#     file_name = generate_qr('http://192.168.0.144:8000/api/v1/receipts/pdf')
#     return FileResponse(f'{file_name}')

@router.get("/pdf/{receipt_id}")
async def get_pdf(receipt_id: str, db=Depends(get_db)):
    path =generate_receipt_pdf(db, receipt_id)
    return FileResponse(path)

@router.post("/", response_model=ReceiptResponse)
async def create_receipt(
    receipt_data: ReceiptCreate,
    db=Depends(get_db),
    current_user = Depends(verify_token)):
    uuid_key = str(generate_uuid())
    user_id = get_user_id(db, current_user)
    db_receipt = Receipt(
        receipt_id=uuid_key,
        user_id=user_id,
        transaction_date=receipt_data.transaction_date,
        total=receipt_data.total,
    )
    
    db.add(db_receipt)
    db.commit()

    pdf_endpoint = generate_qr(f'http://192.168.0.144:8000/api/v1/receipts/pdf/{uuid_key}')
    return JSONResponse({'pdf_endpoint' :pdf_endpoint})