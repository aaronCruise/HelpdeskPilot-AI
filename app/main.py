from fastapi import FastAPI
from app.database import Base, engine
from app.routers.tickets import ticket_router
from app.routers.devices import device_router
from app.routers.checkouts import checkout_router

# Create database & tables
Base.metadata.create_all(bind=engine)

# Start web server
app = FastAPI()

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