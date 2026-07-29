from app.paths import VECTOR_DB_FILE, KNOWLEDGE_BASE_DIR
from app.models.ticket import Ticket
from chromadb import Collection, PersistentClient
from pathlib import Path

NUM_RELEVANT_CHUNKS = 3

def load_documents() -> list:
    documents = []
    p = Path(KNOWLEDGE_BASE_DIR)

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

def create_collection():
    documents = load_documents()
    chunks = chunk_documents(documents)
    chroma_client = PersistentClient(path=VECTOR_DB_FILE)
    collection = chroma_client.get_or_create_collection(name="knowledge_base")

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
    return collection

def get_relevant_chunks(collection: Collection, ticket: Ticket) -> list:
    results = collection.query(
        query_texts=[ticket.text],
        n_results=NUM_RELEVANT_CHUNKS
    )
    return results['documents']