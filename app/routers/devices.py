from app.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate
from app.models.device import Device
from fastapi import APIRouter, HTTPException
from app.database import SessionLocal

device_router = APIRouter()

@device_router.post("/devices/")
async def create_device(device: DeviceCreate):
    try:
        db_session = SessionLocal()
        device_entry = Device(  
            asset_tag = device.asset_tag,
            name = device.name,
            type = device.type
        )
        db_session.add(device_entry)
        db_session.commit()
        db_session.refresh(device_entry)
    finally:
        db_session.close()

    return {
        "message": "device received",
        "device": device_entry
    }

@device_router.get("/devices/")
async def get_devices():
    try:
        db_session = SessionLocal()
        devices_table = db_session.query(Device).all()
    finally:
        db_session.close()
    return {
        "message": "Querying all devices",
        "devices": devices_table
    }

@device_router.get("/devices/{did}", response_model=DeviceRead)
async def get_device_by_id(did: int):
    try:
        db_session = SessionLocal()
        requested_device = db_session.get(Device, did)
        if not requested_device:
            raise HTTPException(
                status_code=404,
                detail="Device not found"
            )
    finally:
        db_session.close()
    return requested_device

@device_router.patch("/devices/{did}", response_model=DeviceUpdate)
async def patch_device(did: int, updates: DeviceUpdate):
    try:
        db_session = SessionLocal()
        requested_device = db_session.get(Device, did)
        if not requested_device:
            raise HTTPException(
                status_code=404,
                detail="Device not found"
            )
        setattr(requested_device, 'state', updates.state)
        db_session.commit()
        db_session.refresh(requested_device)
    finally:
        db_session.close()
    return requested_device