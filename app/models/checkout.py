# Define the checkout model
from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Integer
from app.database import Base

STATUSES = ['active', 'returned', 'overdue', 'cancelled']

class Checkout(Base):
    __tablename__ = 'checkouts'

    cid = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey('devices.did'), nullable=False)
    borrower_name = Column(String, index=True)
    borrower_email = Column(String, index=True)
    from_date = Column(DateTime, index=True)
    to_date = Column(DateTime, index=True)
    status = Column(Enum(*STATUSES), default='active')