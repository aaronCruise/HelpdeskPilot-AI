from fastapi import FastAPI
from app.database import Base, engine
from app.routers.tickets import ticket_router

# Create database & tables
Base.metadata.create_all(bind=engine)

# Start web server
app = FastAPI()

# Use grouped endpoints
app.include_router(ticket_router)

# Create basic GET endpoints
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def read_health():
    return {"status": "ok"}