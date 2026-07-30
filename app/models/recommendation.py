# Define the AI Recommendation Model
from sqlalchemy import Column, DateTime, Enum as SQLEnum, Integer, String, ForeignKey
from datetime import datetime
from app.database import Base
from app.models.ticket import CATEGORIES, PRIORITIES

class Recommendation(Base):
    __tablename__ = 'recommendations'

    rid = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('tickets.tid'), nullable=False, index=True)
    category = Column(SQLEnum(CATEGORIES), index=True, default=CATEGORIES.GENERAL)
    priority = Column(SQLEnum(PRIORITIES), index=True, default=PRIORITIES.MEDIUM)
    summary = Column(String)
    recommended_step = Column(String)
    model_name = Column(String)
    created_at = Column(DateTime, index=True, default=datetime.now)