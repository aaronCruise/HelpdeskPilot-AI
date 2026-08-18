# HelpdeskPilot AI

An AI-powered IT support assistant.
This project automates ticket classification and provides smart recommendations using a RAG pipeline.

### Key Features

- Smart Ticketing: Automatically categorizes and prioritizes incoming IT requests.
- AI Recommendations: Generates suggested next steps for technicians using the Gemini API.
- Knowledge Base Search: Uses RAG to find relevant documentation from internal guides.
- Inventory Management: Tracks hardware assets and equipment checkouts.

### Tech Stack

- Backend: Python, FastAPI, SQLAlchemy (SQLite)
- Frontend: React, Vite
- AI/ML: Google Gemini API, ChromaDB (Vector Store), Ollama (Local fallback)
- Testing: Pytest

### How It Works

1.  Ingestion: Documentation is chunked and stored in a ChromaDB vector database.
2.  Classification: When a ticket is submitted, it is first processed by a rule-based classifier.
3.  Retrieval: The system searches the vector DB for snippets relevant to the ticket text.
4.  Augmentation: The ticket and relevant documentation are sent to the LLM.
5.  Output: The AI returns a refined category, priority, and a recommended action for the technician.

### Getting Started

#### Prerequisites
- Python 3.10+
- Node.js & npm
- Gemini API Key
- [Ollama](https://ollama.com/) installed and running at default port (11434)

#### Running with Docker
```bash
docker-compose up --build
```
The app will be available at http://localhost:5173

#### Local Setup

##### Backend
```bash
echo GEMINI_API_KEY=your_key_here > .env
pip install -r requirements.txt
uvicorn backend.main:app --reload #starts at http://localhost:8000
```

##### Frontend
```bash
cd frontend
npm install
npm run dev #starts at http://localhost:5173
```

### Testing
```bash
pytest backend/tests
```
