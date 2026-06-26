# Define the Ticket model
from sqlalchemy import Column, DateTime, Integer, String
from app.database import Base
import enum


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    requester_name = Column(String, index=True)
    requester_email = Column(String, index=True)
    text = Column(String, index=True)
    category = Column(enum( 'Category', ['general', 'billing', 'technical']), index=True)
    priority = Column(enum('Priority', ['low', 'medium', 'high']), index=True)
    status = Column(enum('Status', ['open', 'in_progress', 'closed']), index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)