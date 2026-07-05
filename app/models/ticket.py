# Define the Ticket model
from sqlalchemy import Column, DateTime, Enum, Integer, String
from datetime import datetime
from app.database import Base

CATEGORIES = ['general', 'billing', 'technical']
PRIORITIES = ['low', 'medium', 'high']
STATUSES = ['new', 'in_progress', 'resolved', 'closed']

class Ticket(Base):
    __tablename__ = 'tickets'

    tid = Column(Integer, primary_key=True, index=True)
    requester_name = Column(String, index=True)
    requester_email = Column(String, index=True)
    text = Column(String, index=True)
    category = Column(Enum(*CATEGORIES), index=True, default='general')
    priority = Column(Enum(*PRIORITIES), index=True, default='medium')
    status = Column(Enum(*STATUSES), index=True, default='new')
    created_at = Column(DateTime, index=True, default=datetime.now())
    updated_at = Column(DateTime, index=True, default=datetime.now(), onupdate=datetime.now())