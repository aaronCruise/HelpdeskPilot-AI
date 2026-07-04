from datetime import datetime
from pydantic import BaseModel, field_validator

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
        return text
    

class TicketRead(BaseModel):
    tid: int
    requester_name: str
    requester_email: str
    text: str
    category: str
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime

class TicketUpdate(BaseModel):
    status: str
    priority: str