from app.schemas.ticket import TicketCreate, TicketRead
from app.models.ticket import Ticket
from fastapi import APIRouter
from app.database import SessionLocal

ticket_router = APIRouter()

@ticket_router.post("/tickets/")
async def create_ticket(ticket: TicketCreate):
    try:
        db_session = SessionLocal()
        ticket_entry = Ticket(  
            requester_name = ticket.requester_name,
            requester_email = ticket.requester_email,
            text = ticket.text
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

@ticket_router.get("/tickets/{tid}")
async def get_ticket_by_id(tid: int):
    try:
        db_session = SessionLocal()
        requested_ticket = db_session.query(Ticket).get(tid)
        if not requested_ticket:
            return {
                "message": "Error: ticket does not exist."
            }
    finally:
        db_session.close()
    return {
        "message": "Getting requested ticket",
        "ticket": requested_ticket
    }