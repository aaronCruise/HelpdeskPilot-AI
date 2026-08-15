from sqlalchemy.orm import Session
from backend.schemas.checkout import CheckoutCreate, CheckoutRead, CheckoutUpdate, CheckIn
from backend.models.checkout import Checkout, STATUSES
from backend.models.device import Device, STATES
from fastapi import APIRouter, HTTPException
from backend.database import SessionLocal

checkout_router = APIRouter()

@checkout_router.post("/checkouts/")
async def create_checkout(checkout: CheckoutCreate):
    try:
        db_session = SessionLocal()
        if not is_device_available(checkout.device_id, db_session):
            raise HTTPException(
                status_code=401,
                detail="Device is not available"
            )
        requested_device = db_session.get(Device, checkout.device_id)
        setattr(requested_device, 'state', STATES.CHECKED_OUT)
        checkout_entry = Checkout(  
            device_id = checkout.device_id,
            borrower_name = checkout.borrower_name,
            borrower_email = checkout.borrower_email,
            from_date = checkout.from_date,
            to_date = checkout.to_date
        )
        db_session.add(checkout_entry)
        db_session.commit()
        db_session.refresh(checkout_entry)
    finally:
        db_session.close()

    return {
        "message": "Checkout received",
        "checkout": checkout_entry
    }

@checkout_router.post("/checkin", response_model=CheckoutRead)
async def check_in(check_in: CheckIn):
    try:
        db_session = SessionLocal()
        requested_checkout = db_session.get(Checkout, check_in.cid)
        if not requested_checkout:
            raise HTTPException(
                status_code=404,
                detail="Checkout not found"
            )
        requested_device = db_session.get(Device, requested_checkout.device_id)
        if requested_device:
            setattr(requested_device, 'state', STATES.AVAILABLE)
        setattr(requested_checkout, 'status', STATUSES.RETURNED)
        db_session.commit()
        db_session.refresh(requested_checkout)
    finally:
        db_session.close()
    return requested_checkout

@checkout_router.get("/checkouts/")
async def get_checkouts():
    try:
        db_session = SessionLocal()
        checkouts_table = db_session.query(Checkout).all()
    finally:
        db_session.close()
    return {
        "message": "Querying all checkouts",
        "checkouts": checkouts_table
    }

@checkout_router.get("/checkouts/active")
async def get_active_checkouts():
    try:
        db_session = SessionLocal()
        active_checkouts_table =\
            db_session.\
                query(Checkout).\
                    where(Checkout.status == STATUSES.ACTIVE).all()
    finally:
        db_session.close()
    return {
        "message": "Querying active checkouts",
        "checkouts": active_checkouts_table
    }

@checkout_router.get("/checkouts/{cid}", response_model=CheckoutRead)
async def get_checkout_by_id(cid: int):
    try:
        db_session = SessionLocal()
        requested_checkout = db_session.get(Checkout, cid)
        if not requested_checkout:
            raise HTTPException(
                status_code=404,
                detail="Checkout not found"
            )
    finally:
        db_session.close()
    return requested_checkout

@checkout_router.patch("/checkout/{cid}", response_model=CheckoutUpdate)
async def patch_checkout(cid: int, updates: CheckoutUpdate):
    try:
        db_session = SessionLocal()
        requested_checkout = db_session.get(Checkout, cid)
        if not requested_checkout:
            raise HTTPException(
                status_code=404,
                detail="Checkout not found"
            )
        setattr(requested_checkout, 'to_date', updates.to_date)
        setattr(requested_checkout, 'status', updates.status)
        db_session.commit()
        db_session.refresh(requested_checkout)
    finally:
        db_session.close()
    return requested_checkout

def is_device_available(device_id: int, db_session: Session) -> bool:
    requested_device = db_session.get(Device, device_id)
    if not requested_device:
        return False
    return bool(requested_device.state == STATES.AVAILABLE)