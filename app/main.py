from fastapi import FastAPI
from app.database import Base, engine
from app.models import checkout, device, ticket

# Create database & tables
Base.metadata.create_all(bind=engine)

# Start web server
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def read_health():
    return {"status": "ok"}