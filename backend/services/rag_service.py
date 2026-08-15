from backend.config import settings
from backend.models.ticket import Ticket
from chromadb import Collection, PersistentClient
from pathlib import Path

chroma_client = PersistentClient(path=str(settings.VECTOR_DB_FILE))
collection = chroma_client.get_or_create_collection(name="knowledge_base")

def load_documents() -> list:
    documents = []
    p = Path(settings.KNOWLEDGE_BASE_DIR)

    for file in p.iterdir():
        if not file.is_file():
            continue
        documents.append(
            {
                'filename': file.name,
                'contents': file.read_text()
            }
        )

    return documents

# Split document lines into chunks with metadata
def chunk_documents(documents) -> list:
    chunks = []
    chunk_index = 0
    for document in documents:
        for line in document['contents'].splitlines():
            if not line:
                continue
            chunks.append(
                {
                    'metadata': {
                        'source': document['filename'],
                        'chunk_index': chunk_index
                    },
                    'text': line
                }
            )
            chunk_index += 1
        chunk_index = 0

    return chunks

def ingest_knowledge_base():
    documents = load_documents()
    chunks = chunk_documents(documents)

    ids = [
        f'{chunk['metadata']['source'].removesuffix('.md')}_{chunk['metadata']['chunk_index']}' 
        for chunk in chunks
        ]
    documents = [chunk['text'] for chunk in chunks]
    metadatas = [chunk['metadata'] for chunk in chunks]

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

def get_relevant_chunks(ticket: Ticket) -> list:
    results = collection.query(
        query_texts=[str(ticket.text)],
        n_results=settings.NUM_RELEVANT_CHUNKS
    )
    relevant_chunks = results["documents"]

    if not relevant_chunks:
        return []

    return relevant_chunks[0]