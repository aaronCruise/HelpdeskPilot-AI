import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

from backend.services.rag_service import ingest_knowledge_base

if __name__ == "__main__":
    print("Ingesting knowledge base...")
    ingest_knowledge_base()
    print("Ingestion complete.")
