from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import engine, Base, SessionLocal
from . import models
from .crud import ingest_event

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)


# ---------- DB Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- Health Check ----------
@app.get("/")
def home():
    return {"message": "Service running"}


# ---------- Event Ingestion ----------
@app.post("/events")
def create_event(event: dict, db: Session = Depends(get_db)):
    result = ingest_event(db, event)
    return {"status": result}


# ---------- List Transactions- Pagination + Sorting ----------
@app.get("/transactions")
def list_transactions(
    merchant_id: str = None,
    status: str = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "created_at",
    order: str = "desc",
    db: Session = Depends(get_db)
):
    query = db.query(models.Transaction)

    if merchant_id:
        query = query.filter(models.Transaction.merchant_id == merchant_id)

    if status:
        query = query.filter(models.Transaction.status == status)

    # Sorting
    if hasattr(models.Transaction, sort_by):
        column = getattr(models.Transaction, sort_by)
        if order == "desc":
            query = query.order_by(column.desc())
        else:
            query = query.order_by(column.asc())

    transactions = query.offset(skip).limit(limit).all()

    return transactions

# ---------- Transaction Details ----------
@app.get("/transactions/{txn_id}")
def get_transaction(txn_id: str, db: Session = Depends(get_db)):
    txn = db.query(models.Transaction).filter_by(transaction_id=txn_id).first()
    events = db.query(models.Event).filter_by(transaction_id=txn_id).all()

    return {
        "transaction": txn,
        "events": events
    }

    return [t.__dict__ for t in transactions]
# ---------- Reconciliation Discrepancies -SQL Optimized Discrepancies---------
@app.get("/reconciliation/discrepancies")
def discrepancies(db: Session = Depends(get_db)):

    txns = db.query(models.Transaction).all()
    discrepancies = []

    for txn in txns:
        events = db.query(models.Event.event_type).filter_by(
            transaction_id=txn.transaction_id
        ).all()

        event_types = [e[0] for e in events]

        # Case 1
        if "payment_processed" in event_types and "settled" not in event_types:
            discrepancies.append(txn.transaction_id)

        # Case 2
        if "payment_failed" in event_types and "settled" in event_types:
            discrepancies.append(txn.transaction_id)

    return {"discrepancies": discrepancies}

#-----reconciliation/summary"------------------

@app.get("/reconciliation/summary")
def reconciliation_summary(db: Session = Depends(get_db)):

    results = (
        db.query(
            models.Transaction.merchant_id,
            models.Transaction.status,
            func.count(models.Transaction.transaction_id).label("count"),
            func.coalesce(func.sum(models.Transaction.amount), 0).label("total_amount")
        )
        .group_by(models.Transaction.merchant_id, models.Transaction.status)
        .all()
    )

    #  Convert to JSON serializable format
    response = []
    for r in results:
        response.append({
            "merchant_id": r.merchant_id,
            "status": r.status,
            "count": r.count,
            "total_amount": r.total_amount
        })

    return response
