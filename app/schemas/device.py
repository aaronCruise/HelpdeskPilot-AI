from datetime import datetime
from pydantic import BaseModel, field_validator

class DeviceCreate(BaseModel):
    asset_tag: str
    name: str
    type: str

    @field_validator('asset_tag')
    def validate_asset_tag(cls, asset_tag):
        if not asset_tag:
            raise ValueError('Asset tag must be populated.')
        return asset_tag

    @field_validator('name')
    def validate_name(cls, name):
        if not name:
            raise ValueError('Name must be populated.')
        return name

    @field_validator('type')
    def validate_type(cls, type):
        if not type:
            raise ValueError('Type must be populated.')
        return type

class DeviceRead(BaseModel):
    did: int
    asset_tag: str
    name: str
    type: str
    state: str
    created_at: datetime

class DeviceUpdate(BaseModel):
    state: str