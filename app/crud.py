from sqlalchemy.orm import Session
from . import models
from datetime import datetime


# ---------- EVENT INGESTION ----------
def ingest_event(db: Session, event_data: dict):
    # 1. Idempotency check
    existing = db.query(models.Event).filter_by(
        event_id=event_data["event_id"]
    ).first()

    if existing:
        return "duplicate"

    # 2. Save event
    event = models.Event(
        event_id=event_data["event_id"],
        transaction_id=event_data["transaction_id"],
        event_type=event_data["event_type"],
        merchant_id=event_data["merchant_id"],
        timestamp=datetime.fromisoformat(event_data["timestamp"])
    )
    db.add(event)

    # 3. Ensure merchant exists
    merchant = db.query(models.Merchant).filter_by(
        merchant_id=event_data["merchant_id"]
    ).first()

    if not merchant:
        merchant = models.Merchant(
            merchant_id=event_data["merchant_id"],
            merchant_name=event_data["merchant_name"]
        )
        db.add(merchant)

    # 4. Create or update transaction
    txn = db.query(models.Transaction).filter_by(
        transaction_id=event_data["transaction_id"]
    ).first()

    if not txn:
        txn = models.Transaction(
            transaction_id=event_data["transaction_id"],
            merchant_id=event_data["merchant_id"],
            amount=event_data["amount"],
            status=event_data["event_type"],
            created_at=event.timestamp,
            updated_at=event.timestamp
        )
        db.add(txn)
    else:
        txn.status = event_data["event_type"]
        txn.updated_at = event.timestamp

    db.commit()
    return "processed"


# ---------- TRANSACTIONS ----------
def get_transactions(db: Session, merchant_id=None, status=None):
    query = db.query(models.Transaction)

    if merchant_id:
        query = query.filter(models.Transaction.merchant_id == merchant_id)

    if status:
        query = query.filter(models.Transaction.status == status)

    return query.all()


def get_transaction_by_id(db: Session, txn_id: str):
    return db.query(models.Transaction).filter_by(
        transaction_id=txn_id
    ).first()


# ---------- RECONCILIATION SUMMARY ----------
def get_reconciliation_summary(db: Session):
    from sqlalchemy import func

    result = db.query(
        models.Transaction.merchant_id,
        models.Transaction.status,
        func.count().label("count"),
        func.sum(models.Transaction.amount).label("total_amount")
    ).group_by(
        models.Transaction.merchant_id,
        models.Transaction.status
    ).all()

    return [
        {
            "merchant_id": r.merchant_id,
            "status": r.status,
            "count": r.count,
            "total_amount": float(r.total_amount or 0)
        }
        for r in result
    ]


# ---------- DISCREPANCIES ----------
def get_discrepancies(db: Session):
    data = db.query(models.Transaction).filter(
        models.Transaction.status.notin_(["payment_processed", "settled"])
    ).all()

    return {
        "discrepancies": [
            {
                "id": txn.transaction_id,
                "merchant_id": txn.merchant_id,
                "amount": txn.amount,
                "status": txn.status
            }
            for txn in data
        ]
    }
