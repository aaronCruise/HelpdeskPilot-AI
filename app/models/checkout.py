# Define the checkout model
from enum import Enum
from sqlalchemy import Column, DateTime, Enum as SQLEnum, ForeignKey, String, Integer
from app.database import Base

class STATUSES(str, Enum):
    ACTIVE = 'active'
    RETURNED = 'returned'
    OVERDUE = 'overdue'
    CANCELLED = 'cancelled'

class Checkout(Base):
    __tablename__ = 'checkouts'

    cid = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey('devices.did'), nullable=False)
    borrower_name = Column(String, index=True)
    borrower_email = Column(String, index=True)
    from_date = Column(DateTime, index=True)
    to_date = Column(DateTime, index=True)
    status = Column(SQLEnum(STATUSES), default=STATUSES.ACTIVE)