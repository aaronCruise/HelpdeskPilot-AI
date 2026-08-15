# Define the device model
from enum import Enum

from sqlalchemy import Column, DateTime, Enum as SQLEnum, Integer, String

from backend.database import Base
from datetime import datetime

TYPES = ['computer', 'phone', 'tablet', 'accessory']


class STATES(str, Enum):
    CHECKED_OUT = 'checked_out'
    AVAILABLE = 'available'
    MAINTENANCE = 'maintenance'
    RETIRED = 'retired'


class Device(Base):
    __tablename__ = 'devices'

    did = Column(Integer, primary_key=True)
    asset_tag = Column(String, index=True, unique=True)
    name = Column(String)
    type = Column(SQLEnum(*TYPES))
    state = Column(SQLEnum(STATES), default=STATES.AVAILABLE)
    created_at = Column(DateTime, index=True, default=datetime.now)