🚀 Solutions Engineer Assignment

🧠 Overview

This service ingests payment lifecycle events, maintains transaction state, and provides reconciliation APIs.

🏗️ Architecture
    FastAPI (backend)
    SQLAlchemy (ORM)
    SQLite (local DB)
⚙️ Features
    Idempotent event ingestion
    Transaction querying with filters, pagination, sorting
    Reconciliation summary
    Discrepancy detection
▶️ Run Locally
    uvicorn app.main:app --reload
    python load_data.py
📡 APIs
    POST /events
    GET /transactions
    GET /transactions/{id}
    GET /reconciliation/summary
    GET /reconciliation/discrepancies
⚖️ Tradeoffs
    SQLite used for simplicity
    No async DB calls (can be improved)
    In-memory validation for discrepancies (can be optimized further)
🔮 Future Improvements
    Move to PostgreSQL
    Add caching
    Add async processing (Kafka / queues)