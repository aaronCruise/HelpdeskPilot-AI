# Define the device model
from sqlalchemy import Column, DateTime, Enum, Integer, String
from app.database import Base
from datetime import datetime

TYPES = ['computer', 'phone', 'tablet', 'accessory']
STATES = ['checked_out', 'available', 'maintenance', 'retired']

class Device(Base):
    __tablename__ = 'devices'

    did = Column(Integer, primary_key=True)
    asset_tag = Column(String, index=True, unique=True)
    name = Column(String)
    type = Column(Enum(*TYPES))
    state = Column(Enum(*STATES), default='available')
    created_at = Column(DateTime, index=True, default=datetime.now)