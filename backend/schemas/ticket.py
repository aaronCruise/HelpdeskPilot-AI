from datetime import datetime
from pydantic import BaseModel, field_validator
from backend.models.ticket import CATEGORIES, PRIORITIES, STATUSES

# Keeps a single ticket's text from turning into an oversized LLM prompt
MAX_TICKET_TEXT_LENGTH = 2000

class TicketCreate(BaseModel):
    requester_name: str
    requester_email: str
    text: str

    @field_validator('requester_name')
    def validate_name(cls, name):
        if not name:
            raise ValueError('Requester name must be populated.')
        return name

    @field_validator('requester_email')
    def validate_email(cls, email):
        if not email:
            raise ValueError('Requester email must be populated.')
        if '@' not in email:
            raise ValueError('Email must be a valid email.')
        return email

    @field_validator('text')
    def validate_text(cls, text):
        if not text:
            raise ValueError('Request text must be populated.')
        if len(text) > MAX_TICKET_TEXT_LENGTH:
            raise ValueError(f'Request text must be {MAX_TICKET_TEXT_LENGTH} characters or fewer.')
        return text
    

class TicketRead(BaseModel):
    tid: int
    requester_name: str
    requester_email: str
    text: str
    category: CATEGORIES
    priority: PRIORITIES
    status: STATUSES
    created_at: datetime
    updated_at: datetime

class TicketUpdate(BaseModel):
    status: STATUSES
    priority: PRIORITIES