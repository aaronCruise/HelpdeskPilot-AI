from datetime import datetime
from pydantic import BaseModel, field_validator, model_validator

class CheckoutCreate(BaseModel):
    device_id: int
    borrower_name: str
    borrower_email: str
    from_date: datetime
    to_date: datetime

    @field_validator('device_id')
    def validate_device_id(cls, device_id):
        if not device_id:
            raise ValueError('Device ID must be populated.')
        return device_id

    @field_validator('borrower_name')
    def validate_name(cls, borrower_name):
        if not borrower_name:
            raise ValueError('Borrower name must be populated.')
        return borrower_name

    @field_validator('borrower_email')
    def validate_email(cls, borrower_email):
        if not borrower_email:
            raise ValueError('Borrower email must be populated.')
        if '@' not in borrower_email:
            raise ValueError('Email must be a valid email.')
        return borrower_email

    @field_validator('from_date')
    def validate_from_date(cls, from_date):
        if not from_date:
            raise ValueError('From date must be populated.')
        return from_date

    @field_validator('to_date')
    def validate_to_date(cls, to_date):
        if not to_date:
            raise ValueError('To date must be populated.')
        return to_date

    @model_validator(mode='after')
    def validate_date_range(self):
        if self.to_date < self.from_date:
            raise ValueError('To date must be after from date.')
        return self
    
class CheckoutRead(BaseModel):
    cid: int
    device_id: int
    borrower_name: str
    borrower_email: str
    from_date: datetime
    to_date: datetime
    status: str

class CheckoutUpdate(BaseModel):
    to_date: datetime
    status: str

class CheckIn(BaseModel):
    cid: int
    status: str