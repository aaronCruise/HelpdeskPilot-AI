# Define the Ticket model
from enum import Enum
from sqlalchemy import Column, DateTime, Enum as SQLEnum, Integer, String
from datetime import datetime
from app.database import Base

class CATEGORIES(str, Enum):
    GENERAL = 'general'
    BILLING = 'billing'
    TECHNICAL = 'technical'
    HARDWARE = 'hardware'
    SOFTWARE = 'software'
    ACCOUNT = 'account'
    NETWORK = 'network'
    CLASSROOM = 'classroom'
    CHECKOUT = 'checkout'

class PRIORITIES(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class STATUSES(str, Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    RESOLVED = 'resolved'
    CLOSED = 'closed'

class Ticket(Base):
    __tablename__ = 'tickets'

    tid = Column(Integer, primary_key=True, index=True)
    requester_name = Column(String, index=True)
    requester_email = Column(String, index=True)
    text = Column(String, index=True)
    category = Column(SQLEnum(CATEGORIES), index=True, default=CATEGORIES.GENERAL)
    priority = Column(SQLEnum(PRIORITIES), index=True, default=PRIORITIES.MEDIUM)
    status = Column(SQLEnum(STATUSES), index=True, default=STATUSES.NEW)
    created_at = Column(DateTime, index=True, default=datetime.now())
    updated_at = Column(DateTime, index=True, default=datetime.now(), onupdate=datetime.now())