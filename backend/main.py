from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import Base, engine
from backend.routers.tickets import ticket_router
from backend.routers.devices import device_router
from backend.routers.checkouts import checkout_router
from backend.config import settings
import backend.models.ticket
import backend.models.device
import backend.models.checkout
import backend.models.recommendation

# Create database & tables
Base.metadata.create_all(bind=engine)

# Start web server
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

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