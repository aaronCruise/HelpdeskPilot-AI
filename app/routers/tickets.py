from app.schemas.ticket import TicketCreate
from app.models.ticket import Ticket
from fastapi import APIRouter
from app.database import SessionLocal

router = APIRouter()

@router.post("/tickets/")
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