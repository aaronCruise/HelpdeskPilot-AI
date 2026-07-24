from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate
from app.models.ticket import Ticket
from app.services.classification_service import classify_ticket
from fastapi import APIRouter, HTTPException
from app.database import SessionLocal

ticket_router = APIRouter()

@ticket_router.post("/tickets/")
async def create_ticket(ticket: TicketCreate):
    classification = classify_ticket(ticket.text)
    
    try:
        db_session = SessionLocal()
        ticket_entry = Ticket(  
            requester_name = ticket.requester_name,
            requester_email = ticket.requester_email,
            text = ticket.text,
            category = classification['category'],
            priority = classification['priority']
        )
        db_session.add(ticket_entry)
        db_session.commit()
        db_session.refresh(ticket_entry)
    finally:
        db_session.close()

    return {
        "message": "Ticket received",
        "ticket": ticket_entry
    }

@ticket_router.get("/tickets/")
async def get_tickets():
    try:
        db_session = SessionLocal()
        tickets_table = db_session.query(Ticket).all()
    finally:
        db_session.close()
    return {
        "message": "Querying all tickets",
        "tickets": tickets_table
    }

@ticket_router.get("/tickets/{tid}", response_model=TicketRead)
async def get_ticket_by_id(tid: int):
    try:
        db_session = SessionLocal()
        requested_ticket = db_session.get(Ticket, tid)
        if not requested_ticket:
            raise HTTPException(
                status_code=404,
                detail="Ticket not found"
            )
    finally:
        db_session.close()
    return requested_ticket

@ticket_router.patch("/tickets/{tid}", response_model=TicketUpdate)
async def patch_ticket(tid: int, updates: TicketUpdate):
    try:
        db_session = SessionLocal()
        requested_ticket = db_session.get(Ticket, tid)
        if not requested_ticket:
            raise HTTPException(
                status_code=404,
                detail="Ticket not found"
            )
        setattr(requested_ticket, 'status', updates.status)
        setattr(requested_ticket, 'priority', updates.priority)
        db_session.commit()
        db_session.refresh(requested_ticket)
    finally:
        db_session.close()
    return requested_ticket