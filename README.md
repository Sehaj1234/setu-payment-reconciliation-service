🔹 Overview
    This service ingests payment events and maintains transaction state using an event-driven architecture.

    It supports reconciliation features such as summary aggregation and discrepancy detection to identify inconsistent transaction states.

🔹 Architecture Overview
    The system follows an event-driven model:

    1. Events are ingested via API
    2. Stored in Event table (immutable log)
    3. Transaction state is derived from events
    4. Merchant data is normalized

    Components:
    - FastAPI → API layer
    - SQLAlchemy → ORM
    - SQLite → storage (Postgres-ready)

🔹 Data Model
    Merchant
    - merchant_id
    - merchant_name

    Transaction
    - transaction_id
    - merchant_id
    - amount
    - status
    - created_at
    - updated_at

    Event
    - event_id
    - transaction_id
    - event_type
    - timestamp

🔹 Setup Instructions
    git clone https://github.com/Sehaj1234/setu-payment-reconciliation-service.git

    cd setu-assignment

    python -m venv venv
    venv\Scripts\activate

    pip install -r requirements.txt
    uvicorn app.main:app --reload

🔹 API Documentation
    POST /events
    - Ingest payment events
    - Idempotent via event_id

    GET /transactions
    - List transactions with filters

    GET /transactions/{id}
    - Fetch transaction with event history

    GET /reconciliation/summary
    - Aggregated data by merchant + status

    GET /reconciliation/discrepancies
    - Detect inconsistent states

🔹 Deployment
    Deployed using Cloud Run for serverless scalability and cost efficiency.
    
    Build:
    pip install -r requirements.txt

    Start:
    uvicorn app.main:app --host 0.0.0.0 --port 10000

🔹 Assumptions
    - Events are source of truth
    - Latest timestamp defines transaction state
    - No authentication required for assignment

🔹 Tradeoffs
    - SQLite used for simplicity (not scalable)
    - In-memory reconciliation logic (can be optimized via SQL aggregation)
    - No background processing (synchronous updates)

🔹 Future Improvements
    - PostgreSQL + indexing
    - Kafka-based event ingestion
    - Authentication & rate limiting
