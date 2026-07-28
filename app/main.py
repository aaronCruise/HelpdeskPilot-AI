from fastapi import FastAPI
from app.database import Base, engine
from app.routers.tickets import ticket_router
from app.routers.devices import device_router
from app.routers.checkouts import checkout_router
from dotenv import load_dotenv
from app.services.docs_loader_service import load_documents
import app.models.ticket
import app.models.device
import app.models.checkout
import app.models.recommendation

# Load LLM API key into environment
load_dotenv()

# Create database & tables
Base.metadata.create_all(bind=engine)

# Start web server
app = FastAPI()

# Load knowledge base documents
DOCUMENTS = load_documents()

# Mount routers
app.include_router(ticket_router)
app.include_router(device_router)
app.include_router(checkout_router)

# Expose basic endpoints
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def read_health():
    return {"status": "ok"}