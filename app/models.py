from sqlalchemy import Column, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Index

class Merchant(Base):
    __tablename__ = "merchants"

    merchant_id = Column(String, primary_key=True)
    merchant_name = Column(String)

class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True)
    merchant_id = Column(String, index=True)      
    amount = Column(Float)
    status = Column(String, index=True)           
    created_at = Column(DateTime, index=True)     
    updated_at = Column(DateTime)

class Event(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True)
    transaction_id = Column(String, index=True)   
    event_type = Column(String)
    merchant_id = Column(String, index=True)      
    timestamp = Column(DateTime, index=True)      

    __table_args__ = (
        UniqueConstraint('event_id', name='unique_event_id'),
    )
