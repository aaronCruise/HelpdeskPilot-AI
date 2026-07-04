from fastapi import FastAPI, APIRouter
from app.database import Base, engine
from app.models import checkout, device, ticket
from app.routers.tickets import router

# Create database & tables
Base.metadata.create_all(bind=engine)

# Start web server
app = FastAPI()

app.include_router(router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def read_health():
    return {"status": "ok"}