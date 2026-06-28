# Define the checkout model
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer
from app.database import Base

class Device(Base):
    __tablename__ = 'checkouts'

    cid = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    device_id = Column(String, ForeignKey('devices.did'), nullable=False)
    from_date = Column(DateTime, index=True)
    to_date = Column(DateTime, index=True)