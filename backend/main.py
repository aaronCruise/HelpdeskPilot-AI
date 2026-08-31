from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from backend.database import Base, engine
from backend.limiter import limiter
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

# Configure rate limiting (protects the LLM-backed /analyze endpoint from abuse)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

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