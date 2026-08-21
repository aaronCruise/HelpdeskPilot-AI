# syntax=docker/dockerfile:1

FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary backend files
COPY backend ./backend
COPY data ./data

# Ensure the data directory exists for ingestion
RUN mkdir -p data

# Pre-ingest the knowledge base during build
# This ensures the vector DB is ready and avoids heavy work at startup
ENV PYTHONPATH=/app
RUN python3 -m backend.scripts.ingest

FROM python:3.12-slim

WORKDIR /app

# Copy the venv from builder.
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy source and the pre-built vector DB
COPY backend ./backend
COPY --from=builder /app/data ./data
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host=0.0.0.0", "--port=8000"]

