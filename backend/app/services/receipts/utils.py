import uuid
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.services.utils import get_user_id
from app.models.receipt import Receipt

def generate_uuid():
    return uuid.uuid1()

def get_user_stats(db: Session, email: str):
    user_id = get_user_id(db, email)
    if user_id is None:
        return {
            'total': 0,
            'total_today': 0,
            'recent_receipts': []
        }

    total_revenue = db.query(func.sum(Receipt.total)) \
        .filter(Receipt.user_id == user_id) \
        .scalar()
    
    if total_revenue is None:
        total_revenue = 0

    twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)

    total_today = db.query(func.sum(Receipt.total)) \
        .filter(
            Receipt.user_id == user_id,
            Receipt.transaction_date >= twenty_four_hours_ago
            ).scalar()
    
    if total_revenue is None:
        total_revenue = 0

    recent_receipts = db.query(
        Receipt.total,
        Receipt.transaction_date
    ).filter(
        Receipt.user_id == user_id,
        Receipt.transaction_date >= twenty_four_hours_ago
    ).order_by(
        desc(Receipt.transaction_date)
    ).all()

    # Format receipts as list of dicts
    recent_receipts_list = [
        {
            'total': float(r.total),
            'transaction_date': r.transaction_date
        }
        for r in recent_receipts
    ]

    result = {
        'total': total_revenue,
        'total_today': total_today,
        'recent_receipts': recent_receipts_list
    }
    return result


def get_receipts(db: Session, email: str):
    user_id = get_user_id(db, email)
    receipts = db.query(
        Receipt.total,
        Receipt.transaction_date,
        Receipt.receipt_id
    ).filter(
        Receipt.user_id == user_id
    ).order_by(
        desc(Receipt.transaction_date)
    ).all()
    receipts_list = [
        {
            'id' : r.receipt_id,
            'total': float(r.total),
            'transaction_date': r.transaction_date
        }
        for r in receipts
    ]
    return receipts_list
