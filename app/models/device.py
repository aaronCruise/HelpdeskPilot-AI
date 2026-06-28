# Define the device model
from sqlalchemy import Column, Date, Enum, Integer, String
from app.database import Base

TYPES = ['computer', 'phone', 'tablet', 'accessory']
STATES = ['checked_out', 'available', 'in_repair']

class Device(Base):
    __tablename__ = 'devices'

    did = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(Enum(*TYPES))
    state = Column(Enum(*STATES))
    model = Column(String, index=True)
    bought_at = Column(Date, index=True)